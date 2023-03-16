import ApiService from '@/services/api.service';

class ProjectService {
  constructor() {
    this.request = ApiService;
  }

  getProjectList(params = {}) {
    return this.request.get('/projects/', { params });
  }

  create(data) {
    return this.request.post('/projects/', data);
  }

  updateProject(projectId, payload) {
    return this.request.patch(`/projects/${projectId}/`, payload);
  }

  deleteProject(projectId) {
    return this.request.delete(`/projects/${projectId}/`);
  }

  getProjectById(projectId) {
    return this.request.get(`/projects/${projectId}/`);
  }

  getRemainingUnitsInDatasetInProject(projectId, params = {}) {
    return this.request.get(
      `/projects/${projectId}/get_remaining_units_in_dataset/`,
      { params }
    );
  }

  exportProject(id) {
    return this.request.get(`/export_project/${id}/`);
  }

  downloadExportedProject(id) {
    //return this.request.get(`/export_project/${id}/download`)
    //window.open(`/export_project/${id}/download`)

    return this.request
      .get(`/export_project/${id}/download`, { responseType: 'blob' })
      .then(response => {
        const blob = new Blob([response.data], {
          type: response.headers['content-type'],
        });
        const link = document.createElement('a');
        link.setAttribute('target', '_blank');
        link.href = URL.createObjectURL(blob);
        //link.download = label
        link.click();
        URL.revokeObjectURL(link.href);
      })
      .catch(console.error);
  }

  getStats(projectId) {
    return this.request.get(`/projects/${projectId}/get_stats/`);
  }

  getProjectWithStats(projectId) {
    return this.request.get(`/projects_with_stats/${projectId}/`);
  }
}

export default new ProjectService();
