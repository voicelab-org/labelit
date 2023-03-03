<template>
  <div class="player-container">
    <span v-shortkey="['ctrl', 'space']" @shortkey="togglePlay"></span>
    <span v-shortkey="['ctrl', 'arrowleft']" @shortkey="skipBackward"></span>
    <span v-shortkey="['ctrl', 'arrowright']" @shortkey="skipForward"></span>

    <div id="wave-timeline"></div>
    <audio v-if="uses_hls" id="stream-audio-hls" ref="streamAudio"></audio>
    <div v-else id="stream-audio-raw"></div>

    <div v-if="!audioLoading && audioInfo" class="stream-player">
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
          <div>
            <v-slider
              v-model="playbackSpeed"
              prepend-icon="mdi-speedometer"
              :label="playbackSpeed + '%'"
              hide-details
              :max="300"
              :min="50"
              inverse-label
              track-color="#a0dcf8"
            ></v-slider>
          </div>
          <div>
            <v-slider
              v-if="enableRegions"
              v-model="zoomingValue"
              prepend-icon="mdi-magnify-plus"
              :label="'   ' + zoomingValue"
              hide-details
              :max="100"
              :min="0"
              inverse-label
              track-color="#a0dcf8"
            ></v-slider>
          </div>
        </div>

        <div class="player-controls">
          <v-btn rounded color="primary" @click="skipBackward()">
            <v-icon>mdi-skip-backward</v-icon>
          </v-btn>

          <v-btn rounded color="primary" @click="togglePlay()">
            <v-icon v-if="isPlaying">mdi-pause</v-icon>
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
import Hls from 'hls.js';
import StreamWaveForms from '@/components/StreamWaveForms.vue';
import WaveSurfer from 'wavesurfer.js';
import RegionsPlugin from 'wavesurfer.js/dist/plugin/wavesurfer.regions.js';
import Minimap from 'wavesurfer.js/dist/plugin/wavesurfer.minimap.js';
import Timeline from 'wavesurfer.js/dist/plugin/wavesurfer.timeline.js';
import DocumentService from '@/services/document.service.js';
import LabelService from '../services/label.service.js';
import TimerDisplay from './TimerDisplay.vue';
import { mapGetters } from 'vuex';

export default {
  components: {
    StreamWaveForms,
    TimerDisplay,
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
    value: {
      // annotated regions
      type: Array,
      required: true,
    },
    regionTasks: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      playbackSpeed: 100,
      zoomingValue: 0,
      duration: 0,
      hls: null,
      uses_hls: false,
      player: null,
      audioLoading: true,
      audioInfo: null,
      isPlaying: false,
      annotated_regions: this.value,
      are_initial_regions_loaded: false,
    };
  },
  watch: {
    playbackSpeed(newVal) {
      this.player.setPlaybackRate(newVal.toFixed(2) / 100.0);
    },
    zoomingValue(newVal) {
      this.player.zoom(newVal);
    },
    document: {
      deep: true,
      handler() {
        this.fetchAudio();
      },
    },
    value: {
      deep: true,
      handler() {
        this.annotated_regions = this.value;
        this.updateRegions();
      },
    },
  },
  created() {
    this.$store.commit('player/SET_PLAYBACK_TIME', 0);
    if (this.regionTasks.length > 1) {
      alert(
        'Multiple Region tasks are currently not supported in the same project'
      );
    }
  },
  mounted() {
    this.$store.commit('player/SET_PLAYBACK_TIME', 0);
    this.fetchAudio();
  },
  methods: {
    updateRegions() {
      if (!this.annotated_regions.length && this.player) {
        Object.entries(this.player.regions.list).forEach(r => {
          r[1].remove();
        });
      }

      if (this.annotated_regions.length) {
        this.annotated_regions.forEach(r => {
          try {
            parseInt(r.id);
          } catch {
            return;
          }

          let existing_frontend_region = Object.entries(
            this.player.regions.list
          ).find(entry => {
            let id = entry[0];
            let region = entry[1];
            return id != r.id && region.start == r.start && region.end == r.end;
          });

          if (existing_frontend_region) {
            existing_frontend_region.id = r.id;
            return;
          }

          let existing_db_region = Object.keys(this.player.regions.list).find(
            id => {
              return id == r.id;
            }
          );

          if (existing_db_region) return;
          this.player.addRegion({
            id: r.id,
            start: r.start,
            end: r.end,
            resize: this.isAdmin ? false : true,
            drag: this.isAdmin ? false : true,
          });
          if (!this.isAdmin && this.enableRegions) {
            this.setupRemoveListeners();
            //this.setupRegionEventListeners()
          }
        });
        this.are_initial_regions_loaded = true;
      }
      if (this.isAdmin && this.enableRegions) {
        this.player.disableDragSelection();
      }
    },
    fetchAudio() {
      this.$store.commit('player/SET_PLAYBACK_TIME', 0);

      if (this.player) {
        this.player.pause();
      }
      DocumentService.doesUseHls(this.document.id).then(res => {
        if (res.data['use_hls']) {
          this.uses_hls = true;
          this.$nextTick(() => {
            if (Hls.isSupported()) {
              this.hls = new Hls({
                audioLoadingTimeOut: 60000,
                xhrSetup: xhr => {
                  xhr.setRequestHeader(
                    'Authorization',
                    `Bearer ${this.$store.state.auth.accessToken}`
                  );
                },
              });
              this.fetchAudioHls(this.document.id);
            } else {
              alert('Player is not supported by your browser !');
            }
          });
        } else {
          this.uses_hls = false;
          let vm = this;
          this.$nextTick(() => {
            let plugins = [];
            if (this.enableRegions) {
              if (!this.isAdmin) {
                plugins.push(
                  RegionsPlugin.create({
                    regionsMinLength: 0.1,
                    dragSelection: {
                      slop: 5,
                    },
                  })
                );
              } else {
                plugins.push(
                  RegionsPlugin.create({
                    regionsMinLength: 0.1,
                  })
                );
              }
              plugins.push(
                Minimap.create({
                  height: 30,
                  waveColor: '#f5cc89',
                  progressColor: '#faa316',
                  cursorColor: '#999',
                })
              );

              plugins.push(
                Timeline.create({
                  container: '#wave-timeline',
                })
              );
            }
            if (vm.player) {
              vm.player.destroy();
              delete vm.player;
            }
            vm.player = WaveSurfer.create({
              backend: 'MediaElement',
              container: '#stream-audio-raw',
              waveColor: '#a0dcf8',
              progressColor: '#03a9f4',
              hideScrollbar: 'true',
              barWidth: '0',
              minPxPerSec: '1000',
              height: 75,
              closeAudioContext: true,
              cursorColor: '#03a9f4',
              plugins: plugins,
            });
            if (this.enableRegions && !this.isAdmin) {
              this.setupRegionEventListeners();
            }
            if (this.enableRegions && this.isAdmin) {
              this.player.disableDragSelection();
            }
            // vm.player.enableDragSelection()
            vm.fetchAudioRaw();
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
      this.player.on('region-update-end', e => {
        let existing_region = this.annotated_regions.find(r => r.id == e.id);

        let promises = [];
        if (existing_region) {
          existing_region.start = e.start;
          existing_region.end = e.end;
          promises.push(
            LabelService.update(e.id, {
              resourcetype: 'AudioRegionLabel',
              end: e.end,
              start: e.start,
            })
          );
        } else {
          promises.push(
            LabelService.create({
              start: e.start,
              end: e.end,
              resourcetype: 'AudioRegionLabel',
              task: this.regionTasks[0].id,
            }).then(res => {
              this.annotated_regions.push({
                id: res.data.id,
                wavesurfer_region_id: e.id,
                start: e.start,
                end: e.end,
                task: this.regionTasks[0].id, // assuming a single region task for now
              });

              let matching_wavesurfer_region = Object.entries(
                this.player.regions.list
              ).find(entry => {
                return entry[0] == e.id;
              });

              //matching_wavesurfer_region.id = res.data.id
              if (matching_wavesurfer_region) {
                matching_wavesurfer_region[1].remove();
              }
              this.player.addRegion({
                id: res.data.id,
                start: e.start,
                end: e.end,
              });
            })
          );
        }

        Promise.all(promises).then(() => {
          this.setupRemoveListeners();
          this.$emit('input', this.annotated_regions);
        });
      });
    },
    setupRemoveListeners() {
      Object.entries(this.player.regions.list).forEach(entry => {
        let region = entry[1];
        region.on('dblclick', () => {
          LabelService.delete(region.id).then(() => {
            this.annotated_regions = this.annotated_regions.filter(
              r => r.id != region.id
            );
            this.$emit('input', this.annotated_regions);
            region.remove();
          });
          //region.remove()
          // TODO: remove in backend and send input event
        });
      });
    },
    fetchAudioHls() {
      this.audioLoading = true;
      DocumentService.getAudioInfo(this.document.id).then(res => {
        this.audioInfo = res.data;
        this.duration = this.audioInfo.duration;
      });

      this.hls.attachMedia(this.$refs.streamAudio);
      this.hls.on(Hls.Events.MEDIA_ATTACHED, () => {
        this.hls.loadSource(
          DocumentService.getDocumentAudioUrl(this.document.id)
        );
        this.hls.on(Hls.Events.MANIFEST_PARSED, () => {
          this.player = this.$refs.streamAudio;
          this.audioLoading = false;

          this.player.addEventListener('play', () => {
            this.isPlaying = true;
            this.$store.commit('player/SET_IS_PLAYING', this.isPlaying);
          });

          this.player.addEventListener('pause', () => {
            this.isPlaying = false;
            this.$store.commit('player/SET_IS_PLAYING', this.isPlaying);
          });

          this.player.addEventListener('timeupdate', () => {
            this.$store.commit(
              'player/SET_PLAYBACK_TIME',
              this.player.currentTime
            );
          });

          this.player.addEventListener('ended', () => {
            this.player.currentTime = 0;
          });

          this.player.skipForward = function (val) {
            this.currentTime += val;
          };

          this.player.skipBackward = function (val) {
            this.currentTime -= val;
          };

          this.player.setPlaybackRate = function (val) {
            this.playbackRate = val;
          };

          this.hls.on(Hls.Events.FRAG_LOADING, () => {});
        });
      });
    },
    fetchAudioRaw() {
      let vm = this;
      this.audioLoading = true;
      DocumentService.getAudioUrl(vm.document.id).then(res => {
        var data = res.data;
        var waveform = data.waveform;
        this.player.load(data.url, waveform, null);
        this.player.setPlayEnd(0);
        this.player.zoom(this.zoomingValue);
        this.player.setPlaybackRate(this.playbackSpeed.toFixed(2) / 100.0);
        this.player.getCurrentTime();
        this.player.on('ready', () => {
          this.duration = this.player.getDuration();
          this.audioLoading = false;
        });

        this.player.on('play', () => {
          this.isPlaying = true;
          this.$store.commit('player/SET_IS_PLAYING', this.isPlaying);
        });

        this.player.on('pause', () => {
          this.isPlaying = false;
          this.$store.commit('player/SET_IS_PLAYING', this.isPlaying);
        });

        this.player.on('finish', () => {
          this.player.currentTime = 0;
        });

        this.player.on('audioprocess', () => {
          this.$store.commit(
            'player/SET_PLAYBACK_TIME',
            vm.player.getCurrentTime()
          );
        });

        this.player.on('region-click', function (region, e) {
          e.stopPropagation();
          // Play on click, loop on shift click
          e.shiftKey ? region.playLoop() : region.play();
        });

        this.player.on('region-out', () => {
          this.player.pause();
        });
        this.player.on('region-in', () => {
          this.player.play();
        });

        this.player.disableDragSelection();
      });

      // setInterval(() => {
      //   this.$store.commit('player/SET_PLAYBACK_TIME', this.player.getCurrentTime())
      // }, 500);
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
  computed: {
    ...mapGetters({
      isAdmin: 'auth/isAdmin',
    }),
    currentPlayBackTime() {
      return this.$store.state.player.playbackTime;
    },
  },
};
</script>

<style lang="scss" scoped>
.player-container {
  margin: 10px 0;
}

.controls-wrapper {
  margin-top: 10px;
  padding-bottom: 20px;
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
