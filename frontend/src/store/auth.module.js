import ApiService from "@/services/api.service";
import AuthService from "@/services/auth.service";
import LocalStorageService from "@/services/local.storage.service";
import UserService from "@/services/user.service";
import router from "@/router";

const access_token = LocalStorageService.getAccessToken() || null;
const refresh_token = LocalStorageService.getAccessToken() || null;
const user = LocalStorageService.getUser() || null;

export const auth = {
  namespaced: true,
  state: {
    accessToken: access_token,
    refreshToken: refresh_token,
    user: user,
  },
  getters: {
    isAuthenticated(state) {
      return state.accessToken != null;
    },
    isAdmin(state) {
      return state.user.is_staff;
    },
    user(state) {
      return state.user;
    },
  },
  actions: {
    authenticateUser({ commit }, authData) {
      return AuthService.postCredential(authData).then((res) => {
        commit("SET_ACCESS_TOKEN", res.data.access);
        commit("SET_REFRESH_TOKEN", res.data.refresh);
        ApiService.setHeader(res.data.access);
        UserService.getCurrentUser()
          .then(function (response) {
            commit("SET_USER", response.data);
          })
          .catch(function (error) {
            console.log(error);
          });
      });
    },
    logout({ dispatch }) {
      ApiService.removeHeader();
      dispatch("resetState");
      router.push("login");
    },
    resetState({ commit }) {
      commit("CLEAR_ACCESS_TOKEN");
      commit("CLEAR_REFRESH_TOKEN");
      commit("CLEAR_USER");
    },
  },
  mutations: {
    SET_ACCESS_TOKEN(state, accessToken) {
      state.accessToken = accessToken;
      LocalStorageService.saveAccessToken(accessToken);
    },
    SET_REFRESH_TOKEN(state, refreshToken) {
      state.refreshToken = refreshToken;
      LocalStorageService.saveRefreshToken(refreshToken);
    },
    SET_USER(state, payload) {
      state.user = payload;
      LocalStorageService.saveUser(payload);
    },
    CLEAR_ACCESS_TOKEN(state) {
      state.accessToken = null;
      LocalStorageService.removeAccessToken();
    },
    CLEAR_REFRESH_TOKEN(state) {
      state.refreshToken = null;
      LocalStorageService.removeRefreshToken();
    },
    CLEAR_USER(state) {
      state.user = null;
      LocalStorageService.removeUser();
    },
  },
};
