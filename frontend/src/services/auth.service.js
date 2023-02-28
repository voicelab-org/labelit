import ApiService from "@/services/api.service";

class AuthService {
  constructor() {
    this.request = ApiService;
  }

  postCredential(data) {
    return this.request.post("auth/login/", data);
  }

  refreshToken(refreshBody) {
    return this.request.post("auth/login/refresh/", refreshBody);
  }

  logout(refreshToken) {
    return this.request.post("auth/logout/", refreshToken);
  }
}

export default new AuthService();
