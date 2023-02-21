export const player = {
  namespaced: true,
  state: {
    playbackTime: 0,
    isPlaying: false,
  },
  getters: {
    playbackTime(state) {
      return state.playbackTime;
    },
    isPlaying(state) {
      return state.isPlaying;
    },
  },
  mutations: {
    SET_PLAYBACK_TIME(state, playbackTime) {
      state.playbackTime = playbackTime;
      //console.log('SET_PLAYBACK_TIME' ,playbackTime )
    },
    SET_IS_PLAYING(state, isPlaying) {
      state.isPlaying = isPlaying;
    },
  },
};
