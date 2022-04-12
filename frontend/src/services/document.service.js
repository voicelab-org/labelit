import ApiService from '@/services/api.service'
import { baseURL } from '@/app.config';

const path = require('path');

class DocumentService {
  constructor() {
    this.request = ApiService
  }

  doesUseHls(documentId, config = {}) {
    return this.request.get(`/audio/${documentId}/is_using_hls/`, config)
  }

  getDocumentAudioById(documentId, config={responseType: 'blob'}) {
    return this.request.get(`/audio/${documentId}/`, config)
  }

  getDocumentAudioUrl(documentId) {
    return new URL(path.join("audio", documentId.toString()), baseURL).toString();
  }

  getAudioInfo(documentId, config={}) {
    return this.request.get(`/audio/${documentId}/audio_info`, config);
  }

}

export default new DocumentService()
