<template>
  <div class="task-form-container">RT dimensional annotation goes here !</div>
</template>

<script>
import { useVideoPlayer } from '@/composables/video_player.js';

export default {
  name: 'RealtimeVideoDimensionalAnnotationTaskForm',
  setup() {
    // composition API
    const { player } = useVideoPlayer();

    return {
      player,
    };
  },
  components: {},
  mixins: [],
  mounted() {
    console.log('this.player.value', this.player.value);
    this.player.value.on('ended', () => {
      console.log('&ended event');
    });
  },
};
</script>

<style lang="scss">
.task-form-container {
  margin-bottom: 15px;
}
</style>
