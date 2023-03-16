import ApiService from '@/services/api.service';

class TaskService {
  constructor() {
    this.request = ApiService;
  }

  getTaskList(params = {}) {
    return this.request.get('/tasks/', params);
  }

  createTask(data) {
    return this.request.post('/tasks/', data);
  }

  updateTask(taskId, payload) {
    return this.request.patch(`/tasks/${taskId}/`, payload);
  }

  deleteTask(taskId) {
    return this.request.delete(`/tasks/${taskId}` + '/');
  }

  getTaskById(taskId) {
    return this.request.get(`/tasks/${taskId}` + '/');
  }

  getTaskByIdAgreementStatsForBatch(taskId, params = {}) {
    return this.request.get(`/tasks/${taskId}/get_agreement_stats_for_batch/`, {
      params,
    });
  }

  getBatchStats(taskId, params = {}) {
    return this.request.get(`/tasks/${taskId}/get_batch_stats/`, { params });
  }

  getProjectStats(taskId, params = {}) {
    return this.request.get(`/tasks/${taskId}/get_project_stats/`, { params });
  }
}

export default new TaskService();
