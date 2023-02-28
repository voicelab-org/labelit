import ApiService from "./api.service";
import AuthService from "./auth.service";

import store from "@/store/index";
import router from "@/router";

async function handleError(error) {
  const originalRequest = error.config;
  if (
    error.response.status === 401 &&
    originalRequest.url === "auth/login/refresh/" &&
    !originalRequest._retry
  ) {
    originalRequest._retry = true;
    store.dispatch("auth/resetState");
    router.replace("login");
  }
  if (error.response.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true;
    const refreshBody = { refresh: store.state.auth.refreshToken };
    let res = await AuthService.refreshToken(refreshBody);
    store.commit("auth/SET_ACCESS_TOKEN", res.data.access);
    originalRequest.headers["Authorization"] = "Bearer " + res.data.access;
    ApiService.setHeader(res.data.access);
    return ApiService.instance(originalRequest);
  }
  return Promise.reject(error);
}

function handleSuccess(response) {
  return response;
}

export default function setup() {
  ApiService.instance.interceptors.response.use(handleSuccess, handleError);
  ApiService.instance.interceptors.request.use(function (config) {
    const accessToken = store.state.auth.accessToken;
    config.headers.Authorization = "Bearer " + accessToken;

    return config;
  });
}
