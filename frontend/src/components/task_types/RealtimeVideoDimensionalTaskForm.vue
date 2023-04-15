<template>
  <div class="task-form-container">
    <div v-if="step == 0">
      RT dimensional annotation goes here !
      <br />
      Autoplay must be activated in your browser.
      <br />
      <MouseTrackingSlider
        :do-track="do_track_mouse_position"
        v-model="position"
      />
      <v-btn
        @click="
          playVideo();
          do_track_mouse_position = true;
        "
      >
        Play
      </v-btn>
    </div>
    <div v-if="step == 1">SUMMATIVE SLIDER</div>
  </div>
</template>

<script>
import { useVideoPlayer } from '@/composables/video_player.js';
import MouseTrackingSlider from '@/components/task_types/components/MouseTrackingSlider.vue';
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
    };
  },
  components: {
    MouseTrackingSlider,
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
}
</style>
