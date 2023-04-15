<template>
  <div class="task-form-container">
    <div v-if="step == 0">
      <p>Autoplay must be activated in your browser.</p>

      <p />
      <div v-if="!is_realtime_sequence_ended">
        <MouseTrackingSlider
          :do-track="do_track_mouse_position"
          v-model="position"
        />
        <div class="play-container" v-if="!do_track_mouse_position">
          <v-btn
            @click="
              playVideo();
              do_track_mouse_position = true;
            "
          >
            Play
          </v-btn>
        </div>
      </div>
      <div v-if="this.is_realtime_sequence_ended">
        Sequence: {{ current_realtime_sequence }}
        <RealtimeSequenceGraph :sequence="current_realtime_sequence" />
      </div>
    </div>
    <div v-if="step == 1">SUMMATIVE SLIDER</div>
  </div>
</template>

<script>
import { useVideoPlayer } from '@/composables/video_player.js';
import MouseTrackingSlider from '@/components/task_types/components/MouseTrackingSlider.vue';
import RealtimeSequenceGraph from '@/components/task_types/components/RealtimeSequenceGraph.vue';
import TaskForm from '@/components/mixins/TaskForm.js';

export default {
  name: 'RealtimeVideoDimensionalTaskForm',
  setup() {
    // composition API
    const { player, playerOptions } = useVideoPlayer();

    return {
      player,
      playerOptions,
    };
  },
  data() {
    return {
      do_track_mouse_position: false,
      position: 50,
      step: 0,
      current_realtime_sequence: [],
      is_realtime_sequence_ended: false,
    };
  },
  components: {
    MouseTrackingSlider,
    RealtimeSequenceGraph,
  },
  mixins: [TaskForm],
  props: {
    videoPlayerLoadedToggle: {
      type: Boolean,
      required: true,
    },
  },
  created() {
    this.setPlayerOptions();
    this.setupEvents();
  },
  watch: {
    position: {
      handler() {
        this.current_realtime_sequence.push([
          this.player.currentTime(),
          this.position,
        ]);
        /*console.log(
            '&position changed in Realtime...TaskForm: ',
            this.position
        );*/
      },
    },
    playerLoadedToggle: {
      handler() {
        this.setPlayerOptions();
        this.setupEvents();
      },
    },
  },
  methods: {
    setupEvents() {
      this.player.on('ended', () => {
        this.do_track_mouse_position = false;
        this.is_realtime_sequence_ended = true;
      });
    },
    playVideo() {
      setTimeout(
        () => {
          this.player.currentTime(0);
          this.setupEvents();
          this.player.play();
        },
        10 // HACK
      );
    },
    setPlayerOptions() {
      let current_options = this.player.options();

      if (current_options.controls) {
        this.playerOptions = this.player.options({
          controls: false, //TODO: uncomment, leaving controls for debugging only
        });
      }
    },
  },
};
</script>

<style lang="scss">
.task-form-container {
  margin-bottom: 15px;

  .play-container {
    display: flex;
    justify-content: center;
  }
}
</style>
