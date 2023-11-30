<template>
  <div id="video-player-container">
    <video-player
      ref="videoPlayer"
      class="video-player-box"
      :options="playerOptions"
      @ready="playerReady"
    >
    </video-player>
  </div>
</template>

<script>
import DocumentService from '@/services/document.service.js';
import { useVideoPlayer } from '@/composables/video_player.js';

export default {
  name: 'LabelitVideoPlayer',
  props: {
    document: {
      type: Object,
      required: true,
    },
  },
  setup() {
    const { setPlayer, player, playerOptions } = useVideoPlayer();

    return {
      setPlayer,
      player,
      playerOptions,
    };
  },
  watch: {
    document: {
      deep: true,
      handler() {
        this.fetchVideo();
      },
    },
  },
  methods: {
    async playerReady(player) {
      this.setPlayer(player);
      await this.fetchVideo();
      this.$emit('player-loaded');
    },
    async fetchVideo() {
      const {
        data: { url },
      } = await DocumentService.getVideoUrl(this.document.id);
      this.player.src({ type: 'video/mp4', src: url });
    },
  },
};
</script>

<style lang="scss">
#video-player-container {
  display: flex;
  justify-content: space-around;
}
</style>
