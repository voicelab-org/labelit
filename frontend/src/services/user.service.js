import ApiService from '@/services/api.service';

class UserService {
  constructor() {
    this.request = ApiService;
  }

  getUserList(params = {}) {
    return this.request.get('/users/', params);
  }

  createUser(data) {
    return this.request.post('/users/', data);
  }

  updateUser(usersId, payload) {
    return this.request.patch(`/users/${usersId}/`, payload);
  }

  deleteUser(usersId) {
    return this.request.delete(`/users/${usersId}/`);
  }

  getUserById(usersId) {
    return this.request.get(`/users/${usersId}/`);
  }

  getCurrentUser() {
    return this.request.get(`/users/me/`);
  }
}

export default new UserService();
