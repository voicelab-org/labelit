<template>
  <div class="qa-form-container">
    <div>
      <div v-if="!is_invalidating">
        <v-btn v-if="!a.has_qa_validated" @click="validate">
          {{ $t('Validate') }}
        </v-btn>
        <v-btn v-if="!a.has_qa_invalidated" @click="invalidate">
          {{ $t('Invalidate') }}
        </v-btn>
      </div>
      <div v-if="is_invalidating" class="invalidation">
        <textarea v-model="invalidation_comment" />
        <v-btn @click="confirmInvalidation">
          {{ $t('Send for Review') }}
        </v-btn>
      </div>
      <div v-else>
        <div v-if="a.qa_invalidation_comment" class="invalidation-comment">
          {{ a.qa_invalidation_comment }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AnnotationService from '@/services/annotation.service.js';

export default {
  name: 'QAForm',
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      a: this.value,
      is_invalidating: false,
      invalidation_comment: '',
    };
  },
  methods: {
    validate() {
      this.is_invalidating = false;
      this.a.qa_invalidation_comment = '';
      this.a.has_qa_validated = true;
      this.a.has_qa_invalidated = false;
      let payload = JSON.parse(JSON.stringify(this.a));
      payload.annotator = payload.annotator.id;
      AnnotationService.updateAnnotation(this.a.id, payload);
      this.$emit('input', this.a);
    },
    invalidate() {
      this.is_invalidating = true;
    },
    confirmInvalidation() {
      this.a.has_qa_validated = false;
      this.a.has_qa_invalidated = true;
      this.a.qa_invalidation_comment = this.invalidation_comment;
      let payload = JSON.parse(JSON.stringify(this.a));
      payload.annotator = payload.annotator.id;
      AnnotationService.updateAnnotation(this.a.id, payload);
      this.$emit('input', this.a);
      this.is_invalidating = false;
    },
  },
};
</script>

<style lang="scss">
.qa-form-container {
  .invalidation textarea {
    display: block;
    border: 1px solid lightgrey !important;
    margin-top: 20px;
    width: 500px;
    height: 100px;
    padding: 10px;
  }

  .invalidation-comment {
    padding: 10px;
    border: 1px solid lightgrey !important;
    margin-top: 20px;
  }
}
</style>
