<template>
  <video-player
    class="video-player-box"
    ref="videoPlayer"
    :options="playerOptions"
    :playsinline="true"
    @play="onPlayerPlay($event)"
    @pause="onPlayerPause($event)"
    @statechanged="playerStateChanged($event)"
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
    const { player, playerOptions } = useVideoPlayer();

    return {
      player,
      playerOptions,
    };
  },
  mounted() {
    console.log('this is current player instance object', this.player);
  },
  computed: {
    computed_player() {
      return this.$refs.videoPlayer.player;
    },
  },
  methods: {
    // listen event
    onPlayerPlay(player) {
      console.log('player play!', player);
      console.log('current playback time: ', this.player.value.currentTime());
    },
    onPlayerPause(player) {
      console.log('player pause!', player);
    },
    // ...player event

    // or listen state event
    playerStateChanged(playerCurrentState) {
      //console.log('player current update state', playerCurrentState);
    },

    // player is ready
    playerReady(player) {
      console.log('the player is ready', player, this.player);
      this.player.value = player;
      this.$emit('player-loaded');
    },
  },
  watch: {},
};
</script>
