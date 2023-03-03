import ApiService from '@/services/api.service';

class DoneAnnotationService {
  constructor() {
    this.request = ApiService;
    this.page = 0;
  }

  getNext(batch_id) {
    this.page++;
    return this.request.get('/done_annotations/', {
      batch: batch_id,
      page: this.page,
    });
  }
}

export default DoneAnnotationService;
