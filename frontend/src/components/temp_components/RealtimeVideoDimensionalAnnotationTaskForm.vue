<template>
  <div class="task-form-container">RT dimensional annotation goes here !</div>
</template>

<script>
import { useVideoPlayer } from '@/composables/video_player.js';

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
  components: {},
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
    //this.player.value.controls(false)
    this.playerOptions = {
      ...this.playerOptions,
      muted: false,
      controls: true,
    };
    /*this.$nextTick(()=>{

      this.player.value.play()
    })*/
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
