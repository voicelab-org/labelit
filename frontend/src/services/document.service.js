import ApiService from '@/services/api.service';
import { baseURL } from '@/app.config';

class DocumentService {
  constructor() {
    this.request = ApiService;
  }

  getDocumentAudioById(documentId, config = { responseType: 'blob' }) {
    return this.request.get(`/audio/${documentId}/`, config);
  }

  getDocumentAudioUrl(documentId) {
    return new URL(`audio/${documentId}`, baseURL).toString();
  }

  getAudioUrl(documentId, config = {}) {
    return this.request.get(`/audio/${documentId}/serve_url/`, config);
  }
}

export default new DocumentService();
