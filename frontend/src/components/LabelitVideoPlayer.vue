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
import {useVideoPlayer} from '@/composables/video_player.js';

export default {
  name: 'LabelitVideoPlayer',
  props: {
    document: {
      type: Object,
      required: true,
    },
  },
  setup() {
    // composition API
    const {set_player, player, playerOptions} = useVideoPlayer();

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
    //this.fetchVideo()
  },
  methods: {
    // player is ready
    async playerReady(player) {
      this.set_player(player);
      await this.fetchVideo()
      this.$emit('player-loaded');
    },
    async fetchVideo() {
      return new Promise(
          (resolve) => {
            DocumentService.getVideoUrl(this.document.id).then(res => {

              let player_loaded = false
              setInterval(
                  () => {
                    if (this.player.el && !player_loaded) {
                      this.player.src({
                        type: 'video/mp4',
                        src: res.data.url,
                      },)
                      player_loaded = true
                      resolve()
                    }
                  },
                  1000
              )
            });
          }
      )
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
