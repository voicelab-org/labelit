import ApiService from '@/services/api.service';

class TimedTranscriptService {
  constructor() {
    this.request = ApiService;
  }

  create(data) {
    return this.request.post('/timed_transcripts/', data);
  }

  update(timed_transcript_id, payload) {
    return this.request.patch(
      `/timed_transcripts/${timed_transcript_id}/`,
      payload
    );
  }
}

export default new TimedTranscriptService();
