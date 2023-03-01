import ApiService from '@/services/api.service';
import { baseURL } from '@/app.config';

class DocumentService {
  constructor() {
    this.request = ApiService;
  }

  doesUseHls(documentId, config = {}) {
    return this.request.get(`/audio/${documentId}/is_using_hls/`, config);
  }

  getDocumentAudioById(documentId, config = { responseType: 'blob' }) {
    return this.request.get(`/audio/${documentId}/`, config);
  }

  getDocumentAudioUrl(documentId) {
    return new URL(`audio/${documentId}`, baseURL).toString();
  }

  getAudioInfo(documentId, config = {}) {
    return this.request.get(`/audio/${documentId}/audio_info`, config);
  }

  getAudioUrl(documentId, config = {}) {
    return this.request.get(`/audio/${documentId}/serve_url/`, config);
  }
}

export default new DocumentService();
