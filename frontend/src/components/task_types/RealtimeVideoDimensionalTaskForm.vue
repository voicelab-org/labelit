<template>
  <div class="task-form-container">
    RT dimensional annotation goes here !
    <br />
    Autoplay must be activated in your browser.
    <br />
    <MouseTrackingSlider
      :do-track="do_track_mouse_position"
      v-model="position"
    />
    <v-btn @click="do_track_mouse_position = true"> Start</v-btn>
    <v-btn @click="do_track_mouse_position = false"> Stop</v-btn>
    <v-btn
      @click="
        playVideo();
        do_track_mouse_position = true;
      "
    >
      Play
    </v-btn>
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
      are_player_options_set: false,
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
          this.player.play();
        },
        10 // HACK
      );
    },
    setPlayerOptions() {
      if (!this.are_player_options_set) {
        this.playerOptions = this.player.options({
          muted: false,
          //controls: false,  //TODO: uncomment, leaving controls for debugging only
        });
        this.are_player_options_set = true;
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
