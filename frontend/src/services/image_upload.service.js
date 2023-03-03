import ApiService from '@/services/api.service';

class ImageUploadService {
  constructor() {
    this.request = ApiService;
  }

  upload(formData) {
    return this.request.post('/upload_image/', formData);
  }
}

export default new ImageUploadService();
