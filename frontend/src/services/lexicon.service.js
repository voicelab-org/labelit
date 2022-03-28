import ApiService from '@/services/api.service'

class LexiconService {
  constructor() {
    this.request = ApiService
  }

  getList(params = {}) {
    return this.request.get('/lexicons/', {params: params})
  }

  get(id, params = {}) {
    return this.request.get(`/lexicons/${id}`, {params: params})
  }

  create(data) {
    console.log("&d", data)
      return this.request.post('/lexicons/', data)
  }
}

export default new LexiconService()
