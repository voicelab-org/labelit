export const SNACKBAR_TYPE_COLOR = {
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
      state.type = payload.type || SNACKBAR_TYPE_COLOR.SUCCESS;
      state.timeout =
        payload.timeout || payload.type === SNACKBAR_TYPE_COLOR.ERROR
          ? -1
          : 3000;
    },
  },
  actions: {
    showSnackbar({ commit }, payload) {
      commit('SHOW_MESSAGE', payload);
    },
  },
};
