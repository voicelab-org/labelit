<template>
  <video-player
    class="video-player-box"
    ref="videoPlayer"
    :options="playerOptions"
    :playsinline="true"
    @ready="playerReady"
  >
  </video-player>
</template>

<script>
import { useVideoPlayer } from '@/composables/video_player.js';

export default {
  name: 'LabelitVideoPlayer',
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
  data() {
    return {};
  },
  methods: {
    // player is ready
    playerReady(player) {
      this.set_player(player);
      this.$emit('player-loaded');
    },
  },
  watch: {},
};
</script>
