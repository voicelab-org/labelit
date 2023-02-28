import ApiService from "@/services/api.service";

const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";
const USER_TOKEN_KEY = "user";
const BLUE_FILTER_KEY = "blue_filter";

class LocalStorageService {
  constructor() {
    this.request = ApiService;
  }

  getBlueFilterValue() {
    return localStorage.getItem(BLUE_FILTER_KEY);
  }

  setBlueFilterValue(v) {
    localStorage.setItem(BLUE_FILTER_KEY, v);
  }

  getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  }

  saveAccessToken(accessToken) {
    localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  }

  removeAccessToken() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
  }

  getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  }

  saveRefreshToken(refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }

  removeRefreshToken() {
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  }

  getUser() {
    return JSON.parse(localStorage.getItem(USER_TOKEN_KEY));
  }

  saveUser(user) {
    localStorage.setItem(USER_TOKEN_KEY, JSON.stringify(user));
  }

  removeUser() {
    localStorage.removeItem(USER_TOKEN_KEY);
  }
}

export default new LocalStorageService();
