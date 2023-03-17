import ApiService from './api.service';
import AuthService from './auth.service';

import store from '@/store/index';
import { SNACKBAR_TYPE_COLOR } from '@/store/snackbar.module';
import router from '@/router';

async function handleError(error) {
  const originalRequest = error.config;
  if (
    error.response.status === 401 &&
    originalRequest.url === 'auth/login/refresh/' &&
    !originalRequest._retry
  ) {
    originalRequest._retry = true;
    store.dispatch('auth/resetState');
    router.replace('login');
    return;
  }
  if (error.response.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true;
    const refreshBody = { refresh: store.state.auth.refreshToken };
    let res = await AuthService.refreshToken(refreshBody);
    if (!res?.data?.access) {
      return;
    }
    store.commit('auth/SET_ACCESS_TOKEN', res.data.access);
    originalRequest.headers['Authorization'] = 'Bearer ' + res.data.access;
    ApiService.setHeader(res.data.access);
    return ApiService.instance(originalRequest);
  }
  if (error.response.status === 500) {
    store.dispatch('snackbar/showSnackbar', {
      text: 'Something went wrong while contacting the server. If the error persists, please contact the support.',
      type: SNACKBAR_TYPE_COLOR.ERROR,
    });
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
    config.headers.Authorization = 'Bearer ' + accessToken;

    return config;
  });
}
