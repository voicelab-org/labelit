import { ref } from 'vue';

// cross-component state
const player = ref({});

export function useVideoPlayer() {
  return {
    player,
  };
}
