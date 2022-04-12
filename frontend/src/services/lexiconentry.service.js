import ApiService from '@/services/api.service'

class LexiconEntryService {
  constructor() {
    this.request = ApiService
  }

  create(data) {
      return this.request.post('/lexicon_entries/', data)
  }

  delete(id){
    return this.request.delete(`/lexicon_entries/${id}`+'/')
  }
}

export default new LexiconEntryService()
