import { ref } from 'vue';

// cross-component state
const player = ref(null);
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
  function set_player(p) {
    console.log('&setting player to: ', p);
    player.value = p;
    player.value.on('play', () => {
      console.log('&&play cb from composable');
    });
  }

  function register_player_event_callback(eventName, callback) {
    console.log('&registering event inside composable', eventName);
    player.value.on(eventName, callback);
  }

  return {
    register_player_event_callback,
    set_player,
    player,
    playerOptions,
  };
}
