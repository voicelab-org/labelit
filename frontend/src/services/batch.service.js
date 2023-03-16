import ApiService from '@/services/api.service';

class BatchService {
  constructor() {
    this.request = ApiService;
  }

  getBatchList(params = {}) {
    return this.request.get('/batches/', { params });
  }

  createBatch(data) {
    return this.request.post('/batches/', data);
  }

  updateBatch(batchId, payload) {
    return this.request.patch(`/batches/${batchId}/`, payload);
  }

  deleteBatch(batchId) {
    return this.request.delete(`/batches/${batchId}/`);
  }

  getBatchById(batchId) {
    return this.request.get(`/batches/${batchId}/`);
  }

  getBatchNextDocument(batchId) {
    return this.request.get(
      `/batches/${batchId}/get_next_document_to_annotate/`
    );
  }

  getNextDocumentToQA(batchId, skipped_document_ids = [], params = {}) {
    return this.request.get(`/batches/${batchId}/get_next_document_to_qa/`, {
      params: {
        skipped_document_ids: skipped_document_ids.join(','),
        ...params,
      },
    });
  }

  getNextDocumentToReview(batchId) {
    return this.request.get(`/batches/${batchId}/get_next_document_to_review/`);
  }

  getNumToReview(batchId) {
    return this.request.get(`/batches/${batchId}/get_num_to_review/`);
  }

  getDocumentToUndo(batchId) {
    return this.request.get(`/batches/${batchId}/get_document_to_undo/`);
  }

  getBatchByIdProgress(batchId) {
    return this.request.get(`/batches/${batchId}/get_progress/`);
  }

  getNumberOfAnnotationsForUser(batchId) {
    return this.request.get(`/batches/${batchId}/get_num_done_annotations/`);
  }

  getStats(batchId) {
    return this.request.get(`/batches/${batchId}/get_stats/`);
  }
}

export default new BatchService();
