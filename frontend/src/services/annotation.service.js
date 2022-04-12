import ApiService from '@/services/api.service'

class AnnotationService {
  constructor() {
    this.request = ApiService
  }

  getAnnotationList(params = {}) {
    return this.request.get('/annotations/', params)
  }

  createAnnotation(data) {
    return this.request.post('/annotations/', data)
  }

  updateAnnotation(annotationId, payload) {
    return this.request.patch(`/annotations/${annotationId}/`, payload)
  }

  deleteAnnotation(annotationId) {
    return this.request.delete(`/annotations/${annotationId}/`)
  }

  getAnnotationById(annotationId) {
    return this.request.get(`/annotations/${annotationId}/`)
  }

}

export default new AnnotationService()
