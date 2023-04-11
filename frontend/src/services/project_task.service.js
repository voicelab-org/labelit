import ApiService from '@/services/api.service';

class ProjectTaskService {
  constructor() {
    this.request = ApiService;
  }

  list(params = {}) {
    return this.request.get('/project_tasks/', params);
  }
}

export default new ProjectTaskService();
