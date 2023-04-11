import { ref } from 'vue';

// cross-component state
const player = ref({});
const playerOptions = ref({
  // videojs options
  muted: true,
  language: 'en',
  controls: true,
  //playbackRates: [0.7, 1.0, 1.5, 2.0],
  sources: [
    {
      type: 'video/mp4',
      src: 'https://cdn.theguardian.tv/webM/2015/07/20/150716YesMen_synd_768k_vp8.webm',
    },
  ],
});
export function useVideoPlayer() {
  return {
    player,
    playerOptions,
  };
}
