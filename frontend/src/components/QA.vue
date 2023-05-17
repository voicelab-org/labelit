<template>
  <div id="qa-container">
    <div v-if="noMore">
      {{ $t('No more to QA') }}
    </div>
    <div>
      <v-checkbox v-model="only_non_reviewed_annotations" @change="resetIndex">
        <div slot="label">
          {{ $t('View only non-reviewed annotations') }}
        </div>
      </v-checkbox>
    </div>
    <div v-if="loaded && project && document">
      <div id="doc-container">
        <Document :document="document" :project="project" />
      </div>
      <div v-for="task in tasks" :key="task.id">
        <b>{{ task.name }}</b>
        <div
          v-for="(a, idx) in taskAnnotations(task)"
          :key="a.id"
          :class="getAnnotationClasses(a)"
        >
          <div>{{ a.annotator.first_name }} {{ a.annotator.last_name }}</div>
          <component
            :is="getFormForTask(task)"
            :annotation="a"
            :task="task"
            :submitting="false"
            :read-only="true"
            :document="document"
          />
          <QAForm v-model="taskAnnotations(task)[idx]" />
        </div>
      </div>
      <template v-if="!noMore">
        <v-btn style="margin-right: 5px" @click="skip">
          {{ $t('Skip') }}
        </v-btn>
        <v-btn @click="getNextDocument(false)"> {{ $t('Next') }} </v-btn>
      </template>
    </div>
  </div>
</template>

<script>
import BatchService from '@/services/batch.service.js';
import DoneAnnotationService from '@/services/done_annotation.service.js';
import QAForm from './QAForm.vue';
import Document from './Document.vue';
import QA from './mixins/QA.js';

export default {
  name: 'QA',
  components: {
    QAForm,
    Document,
  },
  mixins: [QA],
  props: {
    batchId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      document: null,
      annotations: null,
      tasks: null,
      loaded: false,
      noMore: false,
      project: null,
      skipped_document_ids: [],
      only_non_reviewed_annotations: true,
      annotation_index: 0,
    };
  },
  created() {
    this.done_annotation_service = new DoneAnnotationService();
    this.getNextDocument();
  },
  methods: {
    resetIndex() {
      this.annotation_index = 0;
    },
    skip() {
      this.getNextDocument(true);
    },
    getNextDocument(skip = false) {
      let vm = this;

      this.$store.commit('entities/CLEAR_ANNOTATED_ENTITIES');
      vm.annotations = null;
      vm.tasks = null;

      if (skip) {
        this.skipped_document_ids.push(this.document.id);
      }

      BatchService.getBatchById(vm.batchId).then(res => {
        vm.project = res.data.project;
      });

      BatchService.getNextDocumentToQA(vm.batchId, this.skipped_document_ids, {
        only_non_reviewed_annotations: this.only_non_reviewed_annotations,
        index: this.annotation_index,
      }).then(response => {
        if (response.data == '') {
          this.noMore = true;
          this.document = null;
          return;
        }
        vm.annotations = response.data.annotations;
        vm.document = response.data.document;
        vm.tasks = response.data.tasks;
        vm.loaded = true;
      });
      this.annotation_index++;
    },
    taskAnnotations(task) {
      return this.annotations.filter(a => a.task == task.id);
    },
    getFormForTask(task) {
      return task.resourcetype + 'Form';
    },
  },
};
</script>

<style lang="scss">
#qa-container {
  .v-btn--disabled.selected {
    border: 2px solid rgb(3, 169, 244);
    color: black !important;
  }
}
</style>
