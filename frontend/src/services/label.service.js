import ApiService from '@/services/api.service'

class BatchService {
  constructor() {
    this.request = ApiService
  }

  create(data) {
    return this.request.post('/labels/', data)
  }

  get(id) {
    return this.request.get(`/labels/${id}/`)
  }

  update(id, payload) {
    return this.request.patch(`/labels/${id}/`, payload)
  }
}

export default new BatchService()
