<template>
  <video-player
    class="video-player-box"
    ref="videoPlayer"
    :options="playerOptions"
    :playsinline="true"
    @play="onPlayerPlay($event)"
    @pause="onPlayerPause($event)"
    @statechanged="playerStateChanged($event)"
    @ready="playerReadied"
  >
  </video-player>
</template>

<script>
import { useVideoPlayer } from '@/composables/video_player.js';

export default {
  name: 'LabelitVideoPlayer',
  setup() {
    // composition API

    const { player } = useVideoPlayer();

    return {
      player,
    };
  },
  data() {
    return {
      playerOptions: {
        // videojs options
        muted: true,
        language: 'en',
        playbackRates: [0.7, 1.0, 1.5, 2.0],
        sources: [
          {
            type: 'video/mp4',
            src: 'https://cdn.theguardian.tv/webM/2015/07/20/150716YesMen_synd_768k_vp8.webm',
          },
        ],
      },
    };
  },
  mounted() {
    console.log('this is current player instance object', this.player);
    this.player.value = this.computed_player;
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
    playerReadied(player) {
      console.log('the player is readied', player, this.player);
      this.$emit('player-loaded');
      // you can use it to do something...
      // player.[methods]
      //console.log("current playback time: ", this.player.currentTime())
      /*this.player.on('ended', ()=>{
        console.log("video ended")
      })*/
    },
  },
};
</script>
