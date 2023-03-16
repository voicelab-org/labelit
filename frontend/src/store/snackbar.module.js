export const SNACKBAR_TYPE = {
  ERROR: 'error',
  SUCCESS: 'success',
  INFO: 'info',
};

export const snackbar = {
  namespaced: true,
  state: {
    text: '',
    type: '',
    timeout: -1,
  },
  mutations: {
    SHOW_MESSAGE(state, payload) {
      state.text = payload.text || 'Unknown notification';
      state.type = payload.type || SNACKBAR_TYPE.SUCCESS;
      state.timeout =
        payload.timeout || payload.type === SNACKBAR_TYPE.ERROR ? -1 : 3000;
    },
  },
  actions: {
    showSnackbar({ commit }, payload) {
      commit('SHOW_MESSAGE', payload);
    },
  },
};
