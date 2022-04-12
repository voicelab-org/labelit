
export const player = {
  namespaced: true,
  state: {
    playbackTime : 0,
  },
  getters : {
    playbackTime(state) {
      return state.playbackTime
    }
  },
  mutations: {
    SET_PLAYBACK_TIME(state, playbackTime) {
      state.playbackTime = playbackTime
    },
  }
};
