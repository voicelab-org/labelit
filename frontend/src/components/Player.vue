<template>
  <div class="player-container">
    <span v-shortkey="['ctrl', 'space',]" @shortkey="togglePlay"></span>
    <span v-shortkey="['ctrl', 'arrowleft',]" @shortkey="skipBackward"></span>
    <span v-shortkey="['ctrl', 'arrowright',]" @shortkey="skipForward"></span>

    <audio v-if="uses_hls" id="stream-audio-hls" ref="streamAudio"></audio>
    <div v-else id="stream-audio-raw"></div>

    <div class="stream-player" v-if="!audioLoading && audioInfo">
      <div class="stream-waves">
        <StreamWaveForms
            :current-play-back-time="currentPlayBackTime"
            :waveform-data="audioInfo.waveform"
            :duration="duration"
            @waveform-clicked="updateTimeByCursor"
        />
      </div>
    </div>

    <div class="controls-wrapper">
      <template v-if="!audioLoading">
        <div class="slider-container">
          <v-slider
              v-model="playbackSpeed"
              prepend-icon="mdi-speedometer"
              :label="playbackSpeed + '%'"
              hide-details
              :max="300"
              :min="50"
              track-color="#a0dcf8"
          ></v-slider>
        </div>
        <div class="player-controls">
          <v-btn rounded color="primary" @click="skipBackward()">
            <v-icon>mdi-skip-backward</v-icon>
          </v-btn>

          <v-btn rounded color="primary" @click="togglePlay()">
            <v-icon v-if="this.isPlaying">mdi-pause</v-icon>
            <v-icon v-else>mdi-play</v-icon>
          </v-btn>

          <v-btn rounded color="primary" @click="skipForward()">
            <v-icon>mdi-skip-forward</v-icon>
          </v-btn>
        </div>
        <div class="duration-container">
          <span class="duration">
            <timer-display
                :seconds="currentPlayBackTime"
                :max="duration"
            ></timer-display>
            /
            <timer-display :seconds="duration"></timer-display>
          </span>
        </div>
      </template>
      <template v-else>
        <div class="progress-bar">
          <v-progress-circular
              v-show="audioLoading"
              indeterminate
              color="primary"
              :size="48"
          ></v-progress-circular>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import Hls from "hls.js";
import StreamWaveForms from '@/components/StreamWaveForms'
import WaveSurfer from "wavesurfer.js";
import RegionsPlugin from "wavesurfer.js/dist/plugin/wavesurfer.regions.js"
import DocumentService from "@/services/document.service"
import LabelService from "../services/label.service";
import TimerDisplay from "./TimerDisplay"


export default {
  components: {
    StreamWaveForms,
    TimerDisplay,
  },
  data() {
    return {
      playbackSpeed: 100,
      duration: 0,
      hls: null,
      uses_hls: false,
      player: null,
      audioLoading: true,
      speedRate: 100,
      audioInfo: null,
      isPlaying: false,
      annotated_regions: this.value,
      are_initial_regions_loaded: false,
    };
  },
  props: {
    document: {
      type: Object,
      required: true,
    },
    enableRegions: {
      type: Boolean,
      default: false,
    },
    value: { // annotated regions
      type: Array,
      required: true,
    },
    regionTasks: {
      type: Array,
      required: true,
    },
  },
  created() {
    if (this.regionTasks.length > 1) {
      alert("Multiple Region tasks are currently not supported in the same project")
    }
  },
  mounted() {
    this.fetchAudio()
  },
  methods: {
    updateRegions() {

      if (!this.annotated_regions.length) {
        Object.entries(this.player.regions.list).forEach(
            (r) => {
              r[1].remove()
            }
        )
      }

      if (this.annotated_regions.length) {

        this.annotated_regions.forEach(
            (r) => {
              try {
                parseInt(r.id)
              } catch {
                return
              }

              let existing_frontend_region = Object.entries(this.player.regions.list).find(
                  (entry) => {
                    let id = entry[0]
                    let region = entry[1]
                    return id != r.id && region.start == r.start && region.end == r.end
                  }
              )

              if (existing_frontend_region) {
                existing_frontend_region.id = r.id
                return
              }

              let existing_db_region = Object.keys(this.player.regions.list).find(
                  (id) => {
                    return id == r.id
                  }
              )

              if (existing_db_region) return
              this.player.addRegion(
                  {
                    id: r.id,
                    start: r.start,
                    end: r.end,
                  }
              )

              this.setupRemoveListeners()
              //this.setupRegionEventListeners()
            }
        )
        this.are_initial_regions_loaded = true
      }
    },
    fetchAudio() {
      if (this.player) {
        this.player.pause()
      }
      DocumentService.doesUseHls(this.document.id).then((res) => {
        if (res.data["use_hls"]) {
          this.uses_hls = true;
          this.$nextTick(() => {
            if (Hls.isSupported()) {
              this.hls = new Hls({
                audioLoadingTimeOut: 60000,
                xhrSetup: (xhr) => {
                  xhr.setRequestHeader("Authorization", `Bearer ${this.$store.state.auth.accessToken}`);
                },
              });
              this.fetchAudioHls(this.document.id);
            } else {
              alert("Player is not supported by your browser !");
            }
          });
        } else {
          this.uses_hls = false;
          let vm = this
          this.$nextTick(() => {

            let plugins = []
            if (this.enableRegions) {
              plugins.push(
                  RegionsPlugin.create({
                    regionsMinLength: 0.1,
                    dragSelection: {
                      slop: 5
                    },
                  })
              )
            }
            console.log("creating player")
            if (vm.player){
              vm.player.destroy()
              delete vm.player
            }
            vm.player = WaveSurfer.create({
              container: "#stream-audio-raw",
              waveColor: "#a0dcf8",
              progressColor: "#03a9f4",
              hideScrollbar: 'true',
              barWidth: '0',
              minPxPerSec: '1000',
              height: 100,
              cursorColor: "#03a9f4",
              plugins: plugins
            });
            if (this.enableRegions) {
              this.setupRegionEventListeners()
            }
            // vm.player.enableDragSelection()
            vm.fetchAudioRaw()
            /*vm.player.addRegion(
                {
                  start: 1.0,
                  end: 2.0,
                  color: "rbga(0, 255, 0, 1)",

                }
            )*/
          });
        }
      });
    },
    setupRegionEventListeners() {

      this.player.on("region-update-end", (e) => {
        let existing_region = this.annotated_regions.find(r => r.id == e.id)

        let promises = []
        if (existing_region) {
          existing_region.start = e.start
          existing_region.end = e.end
          promises.push(LabelService.update(e.id, {
            resourcetype: "AudioRegionLabel",
            end: e.end,
            start: e.start
          }))
        } else {
          promises.push(LabelService.create(
              {
                start: e.start,
                end: e.end,
                resourcetype: "AudioRegionLabel",
                task: this.regionTasks[0].id,
              }
          ).then(
              (res) => {
                this.annotated_regions.push(
                    {
                      id: res.data.id,
                      wavesurfer_region_id: e.id,
                      start: e.start,
                      end: e.end,
                      task: this.regionTasks[0].id, // assuming a single region task for now
                    }
                )

                let matching_wavesurfer_region = Object.entries(this.player.regions.list).find(
                    (entry) => {
                      return entry[0] == e.id
                    }
                )

                //matching_wavesurfer_region.id = res.data.id
                if (matching_wavesurfer_region) {
                  matching_wavesurfer_region[1].remove()
                }
                this.player.addRegion({
                  id: res.data.id,
                  start: e.start,
                  end: e.end,
                })
              }
          ))

        }

        Promise.all(promises).then(() => {
          this.setupRemoveListeners()
          this.$emit('input', this.annotated_regions)
        })

      });
    },
    setupRemoveListeners() {
      Object.entries(this.player.regions.list).forEach(
          (entry) => {
            let region = entry[1]
            region.on('dblclick', () => {
              LabelService.delete(region.id).then(
                  () => {
                    this.annotated_regions = this.annotated_regions.filter(r => r.id != region.id)
                    this.$emit('input', this.annotated_regions)
                    region.remove()
                  }
              )
              //region.remove()
              // TODO: remove in backend and send input event
            })
          }
      )
    },
    fetchAudioHls() {
      this.audioLoading = true;
      DocumentService.getAudioInfo(this.document.id)
          .then((res) => {
            this.audioInfo = res.data;
            this.duration = this.audioInfo.duration;
          });

      this.hls.attachMedia(this.$refs.streamAudio);
      this.hls.on(Hls.Events.MEDIA_ATTACHED, () => {
        this.hls.loadSource(DocumentService.getDocumentAudioUrl(this.document.id));
        this.hls.on(Hls.Events.MANIFEST_PARSED, () => {
          this.player = this.$refs.streamAudio;
          this.audioLoading = false;

          this.player.addEventListener("play", () => {
            this.isPlaying = true;
            this.$store.commit('player/SET_IS_PLAYING', this.isPlaying)
          });

          this.player.addEventListener("pause", () => {
            this.isPlaying = false;
            this.$store.commit('player/SET_IS_PLAYING', this.isPlaying)
          });

          this.player.addEventListener("timeupdate", () => {
            this.$store.commit('player/SET_PLAYBACK_TIME', this.player.currentTime);
          });

          this.player.addEventListener("ended", () => {
            this.player.currentTime = 0;
          });

          this.player.skipForward = function (val) {
            this.currentTime += val;
          }

          this.player.skipBackward = function (val) {
            this.currentTime -= val;
          }

          this.player.setPlaybackRate = function (val) {
            this.playbackRate = val;
          }

          this.hls.on(Hls.Events.FRAG_LOADING, () => {
          });
        });
      });
    },
    fetchAudioRaw() {
      let vm = this
      this.audioLoading = true;
      DocumentService.getDocumentAudioById(vm.document.id)
          .then((res) => {
            vm.player.loadBlob(res.data);

            this.player.on("ready", () => {
              this.duration = vm.player.getDuration();
              vm.audioLoading = false;
            });

            this.player.on("play", () => {
              this.isPlaying = true;
              this.$store.commit('player/SET_IS_PLAYING', this.isPlaying)
            });

            this.player.on("pause", () => {
              this.isPlaying = false;
              this.$store.commit('player/SET_IS_PLAYING', this.isPlaying)
            });

            this.player.on("finish", () => {
              this.player.currentTime = 0;
            });
          })

      setInterval(() => {
        vm.$store.commit('player/SET_PLAYBACK_TIME', vm.player.getCurrentTime())
      }, 500);
    },
    skipForward() {
      this.player.skipForward(1);
    },
    skipBackward() {
      this.player.skipBackward(1);
    },
    togglePlay() {
      if (this.isPlaying) {
        this.player.pause();
      } else {
        this.player.play();
      }
    },
    updateTimeByCursor(newTime) {
      this.player.currentTime = newTime;
    },
  },
  watch: {
    playbackSpeed(newVal) {
      this.player.setPlaybackRate(newVal.toFixed(2) / 100.0);
    },
    document: {
      deep: true,
      handler() {
        this.fetchAudio()
      },
    },
    value: {
      deep: true,
      handler() {
        this.annotated_regions = this.value
        this.updateRegions()
      }
    },
    /*'player.regions.list': {
      deep: true,
      handler(){
        console.log("&regions changed")
        console.log("&&list", JSON.stringify(this.player.regions.list))
        Object.entries(this.player.regions.list).forEach(
            (entry) => {
              console.log("entry", entry)
              let region = entry[1]
              console.log("&region", region)
              region.on('dblclick', () => {
                console.log("&removing!!!")
                //region.remove()
                // TODO: remove in backend and send input event
              })
            }
        )
      }
    }*/
  },
  computed: {
    currentPlayBackTime() {
      return this.$store.state.player.playbackTime;
    },
  }
};
</script>

<style lang="scss" scoped>

.player-container {
  margin: 10px 0;
}

.controls-wrapper {
  margin-top: 10px;
  position: relative;

  .slider-container {
    position: absolute;
    top: 3px;
    left: 0;
    min-width: 200px;
  }

  .player-controls {
    flex: 2;
    display: flex;
    justify-content: center;
    align-items: center;

    .v-btn {
      margin: 0 5px;
    }
  }

  .duration-container {
    position: absolute;
    top: 3px;
    right: 0;
    align-items: center;
    text-align: right;

    > div {
      margin-left: auto;
    }

    > span.duration {
      margin-left: auto;
    }
  }

  .progress-bar {
    flex: 2;
    display: flex;
    justify-content: center;
    align-items: center;

    .v-btn {
      margin: 0 5px;
    }
  }
}
</style>