import { ref } from 'vue';

// cross-component state
const player = ref(null);
const playerOptions = ref({
  // videojs options
  muted: false,
  language: 'en',
  controls: true,
  sources: [
    {
      type: 'video/mp4',
      // src: 'http://techslides.com/demos/sample-videos/small.mp4',
      src: '/small_black.mp4',
    },
  ],
});

export function useVideoPlayer() {
  function set_player(p) {
    player.value = p;
  }

  return {
    set_player,
    player,
    playerOptions,
  };
}
