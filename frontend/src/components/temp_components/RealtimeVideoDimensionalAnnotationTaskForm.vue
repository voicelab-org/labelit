<template>
  <div class="task-form-container">
    RT dimensional annotation goes here !
    <br />
    <MouseTrackingSlider
      :do-track="do_track_mouse_position"
      v-model="position"
    />
    <v-btn @click="do_track_mouse_position = true">Start</v-btn>
    <v-btn @click="do_track_mouse_position = false">Stop</v-btn>
    <v-btn
      @click="
        play();
        do_track_mouse_position = true;
      "
      >Play</v-btn
    >
  </div>
</template>

<script>
import { useVideoPlayer } from '@/composables/video_player.js';
import MouseTrackingSlider from '@/components/task_types/components/MouseTrackingSlider.vue';

export default {
  name: 'RealtimeVideoDimensionalAnnotationTaskForm',
  setup() {
    // composition API
    const { player, playerOptions, register_player_event_callback } =
      useVideoPlayer();

    return {
      register_player_event_callback,
      player,
      playerOptions,
    };
  },
  data() {
    return {
      do_track_mouse_position: false,
      position: 50,
    };
  },
  components: {
    MouseTrackingSlider,
  },
  mixins: [],
  mounted() {
    console.log('&this.player', this.player);

    this.register_player_event_callback('play', () => {
      console.log('&play from task form!');
    });

    //this.player.on('play', ()=>{console.log("&play!")})

    /*
      console.log(
        '&this.player.value',
        JSON.parse(JSON.stringify(this.player.value))
      );
      console.log(
        'player options',
        JSON.parse(JSON.stringify(this.playerOptions))
      );
      this.player.value.on('ended', () => {
        console.log('&ended event');
      });
    */

    /*this.playerOptions = {
      ...this.playerOptions,
      muted: false,
      controls: true,
    };*/

    /*
      this.player.value.on('ended', () => {
        console.log('&ended event');
        this.do_track_mouse_position = false
      });
      this.player.value.on('enterFullWindow', () => {
        console.log('&enterFullWindow event');
        //this.do_track_mouse_position = false
      });
      this.player.value.on('play', () => {
        console.log('&play event');
        //this.do_track_mouse_position = false
      });

      this.player.value.on('pause', () => {
        console.log('&pause event');
        //this.do_track_mouse_position = false
      });
     */

    //enterFullWindow
    /*
      setTimeout(() => {
        this.player.value.play();
      }, 300);
    */
  },
  watch: {
    position: {
      handler() {
        console.log(
          '&position changed in Realtime...TaskForm: ',
          this.position
        );
      },
    },
  },
  methods: {
    play() {
      setTimeout(
        () => {
          this.player.currentTime(0);
          this.player.play();
        },
        10 // HACK
      );
    },
  },
};
</script>

<style lang="scss">
.task-form-container {
  margin-bottom: 15px;
}
</style>
