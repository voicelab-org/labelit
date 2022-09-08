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
  created(){
    if (this.regionTasks.length > 1){
      alert("Multiple Region tasks are not supported in the same project")
    }
  },
  mounted() {
    this.fetchAudio()
  },
  methods: {
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
            if (this.enableRegions){
              plugins.push(
                RegionsPlugin.create({
                  regionsMinLength: 0.1,
                  /*regions: [
                    {
                      start: 0.2,
                      end: 0.5,
                      loop: false,
                      color: 'hsla(400, 100%, 30%, 0.5)'
                    }, {
                      start: 0.6,
                      end: 1.2,
                      loop: false,
                      color: 'hsla(200, 50%, 70%, 0.4)',
                      minLength: 1,
                      maxLength: 5,
                    }
                  ],*/
                  dragSelection: {
                    slop: 5
                  },
                })
              )
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
            if (this.enableRegions){
              this.setupRegionEventListeners()
            }
            // vm.player.enableDragSelection()
            vm.fetchAudioRaw()
          });
        }
      });
    },
    setupRegionEventListeners(){
      /*
      region-created
      region-updated
      region-update-end
      region-removed

       */
      /*
        this.player.on("region-created", (e) => {
          console.log("region created", e)
          console.log("start & end", e.start, e.end)
        });
        this.player.on("region-updated", (e) => {
          console.log("region updated", e)
          console.log("start & end", e.start, e.end)
        });
      */
      this.player.on("region-update-end", (e) => {
        console.log("region update end", e)
        console.log("start & end", e.start, e.end)
        this.annotated_regions.push(
            {
              wavesurfer_region_id: e.id,
              start: e.start,
              end: e.end,
            }
        )
        console.log("this.annotated_regions", this.annotated_regions)
        this.$emit('input', this.annotated_regions)
      });
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

          });

          this.player.addEventListener("pause", () => {
            this.isPlaying = false;
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
      console.log("fetch raw")
      let vm = this
      this.audioLoading = true;
      DocumentService.getDocumentAudioById(vm.document.id)
          .then((res) => {
            console.log("res", res.data)
            vm.player.loadBlob(res.data);

            this.player.on("ready", () => {
              this.duration = vm.player.getDuration();
              vm.audioLoading = false;
            });

            this.player.on("play", () => {
              this.isPlaying = true;
            });

            this.player.on("pause", () => {
              this.isPlaying = false;
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
  },
  computed: {
    currentPlayBackTime() {
      return this.$store.state.player.playbackTime;
    },
  }
};
</script>

<style lang="scss" scoped>

.player-container{
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