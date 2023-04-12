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
    const { set_player, player, playerOptions } = useVideoPlayer();

    return {
      set_player,
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
  data() {
    return {
      count_ready: 0,
    };
  },
  methods: {
    // listen event
    onPlayerPlay(player) {
      console.log('player play!', player);
      console.log('current playback time: ', this.player.currentTime());
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
      console.log('the player is ready', player, player === this.player);

      this.count_ready++;

      console.log('count ready: ', this.count_ready);

      //if (this.count_ready == 2){ //HACK
      this.set_player(player);
      this.$emit('player-loaded');
      //}

      /*
      setTimeout(  // HACK
          () => {
            this.$emit('player-loaded');
          },
          50,
      )
       */
    },
  },
  watch: {},
};
</script>
