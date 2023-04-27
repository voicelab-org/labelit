<template>
  <div id="video-player-container">
    <video-player
      class="video-player-box"
      ref="videoPlayer"
      :options="playerOptions"
      :playsinline="true"
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
      //required: true,
    },
  },
  setup() {
    // composition API
    const { set_player, player, playerOptions } = useVideoPlayer();

    return {
      set_player,
      player,
      playerOptions,
    };
  },
  computed: {
    computed_player() {
      return this.$refs.videoPlayer.player;
    },
  },
  created() {
    this.fetchVideo();
  },
  methods: {
    // player is ready
    playerReady(player) {
      this.set_player(player);
      this.$emit('player-loaded');
    },
    fetchVideo() {
      DocumentService.getVideoUrl(this.document.id).then(res => {
        this.playerOptions = this.player.options({
          sources: [
            {
              type: 'video/mp4',
              src: res.data.url,
            },
          ],
        });
      });
    },
  },
  watch: {
    document: {
      deep: true,
      handler() {
        this.fetchVideo();
      },
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
