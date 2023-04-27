import { ref } from 'vue';

// cross-component state
const player = ref(null);
const playerOptions = ref({
  // videojs options
  muted: false,
  language: 'en',
  controls: true,
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
