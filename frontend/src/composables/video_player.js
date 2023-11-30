import { ref } from 'vue';

// cross-component state
const player = ref(null);
const playerOptions = ref({
  muted: false,
  language: 'en',
  controls: true,
  playsinline: true,
});

export function useVideoPlayer() {
  function setPlayer(newPlayer) {
    player.value = newPlayer;
  }

  return {
    setPlayer,
    player,
    playerOptions,
  };
}
