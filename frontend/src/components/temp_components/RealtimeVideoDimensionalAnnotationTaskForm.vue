<template>
  <div class="task-form-container">
    RT dimensional annotation goes here !
    <br />
    <MouseTrackingSlider :do-track="do_start" v-model="position" />
    <v-btn @click="do_start = true">Start</v-btn>
    <v-btn @click="do_start = false">Stop</v-btn>
  </div>
</template>

<script>
import { useVideoPlayer } from '@/composables/video_player.js';

import MouseTrackingSlider from '@/components/task_types/components/MouseTrackingSlider.vue';

export default {
  name: 'RealtimeVideoDimensionalAnnotationTaskForm',
  setup() {
    // composition API
    const { player, playerOptions } = useVideoPlayer();

    console.log('&player options 1', playerOptions.value);

    return {
      player,
      playerOptions,
    };
  },
  data() {
    return {
      do_start: false,
      position: 0,
    };
  },
  components: {
    MouseTrackingSlider,
  },
  mixins: [],
  mounted() {
    console.log(
      'this.player.value',
      JSON.parse(JSON.stringify(this.player.value))
    );
    console.log(
      'player options',
      JSON.parse(JSON.stringify(this.playerOptions))
    );
    this.player.value.on('ended', () => {
      console.log('&ended event');
    });
    this.playerOptions = {
      ...this.playerOptions,
      muted: false,
      controls: true,
    };
    setTimeout(() => {
      this.player.value.play();
    }, 300);
  },
};
</script>

<style lang="scss">
.task-form-container {
  margin-bottom: 15px;
}
</style>
