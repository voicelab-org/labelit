export const snackbar = {
  namespaced: true,
  state: {
    text: '',
    color: '',
    timeout: -1,
  },
  mutations: {
    SHOW_MESSAGE(state, payload) {
      state.text = payload.text || 'Unknown notification';
      state.color = payload.color || 'success';
      state.timeout = payload.timeout || 3000;
    },
  },
  actions: {
    showSnackbar({ commit }, payload) {
      commit('SHOW_MESSAGE', payload);
    },
  },
};
