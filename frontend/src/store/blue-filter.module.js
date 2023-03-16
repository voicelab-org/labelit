import LocalStorageService from '@/services/local.storage.service.js';

export const blueFilter = {
  namespaced: true,
  state: {
    percentage: LocalStorageService.getBlueFilterValue() || 45,
  },
  getters: {
    percentage(state) {
      return state.percentage;
    },
  },
  mutations: {
    SET_PERCENTAGE(state, percentage) {
      LocalStorageService.setBlueFilterValue(percentage);
      state.percentage = percentage;
    },
  },
};
