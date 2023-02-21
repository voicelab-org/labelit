import ApiService from "@/services/api.service";

class DatasetService {
  constructor() {
    this.request = ApiService;
  }

  getDatasetList(params = {}) {
    return this.request.get("/datasets/", params);
  }

  createDataset(data) {
    return this.request.post("/datasets/", data);
  }

  updateDataset(datasetId, payload) {
    return this.request.patch(`/datasets/${datasetId}/`, payload);
  }

  deleteDataset(datasetId) {
    return this.request.delete(`/datasets/${datasetId}/`);
  }

  getDatasetById(datasetId) {
    return this.request.get(`/datasets/${datasetId}/`);
  }
}

export default new DatasetService();
