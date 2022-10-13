<template>
  <div id="qa-container">
  <div v-if="noMore">
            No more to QA
        </div>
    <div>

      <v-checkbox v-model="only_non_reviewed_annotations" @change="resetIndex">
        <div slot="label">
          View only non-reviewed annotations
        </div>
      </v-checkbox>
    </div>
    <div v-if="loaded && project">
            <div id="doc-container" v-if="document">
                <Document :document="document" :project="project" />
            </div>
            <div v-for="task in tasks" :key="task.id">
                <b>{{task.name}}</b>
                <div v-for="(a, idx) in taskAnnotations(task)" :key="a.id" :class="getAnnotationClasses(a)">
                    <div>
                        {{a.annotator.first_name}} {{a.annotator.last_name}}
                    </div>
                    <component
                         :is="getFormForTask(task)"
                         :annotation="a"
                         :task="task"
                         :submitting="false"
                         :read-only="true"
                    />
                    <QAForm
                        v-model="taskAnnotations(task)[idx]"
                    />
                </div>
            </div>
            <template v-if="!noMore">
              <v-btn @click="skip" style="margin-right: 5px"> Skip </v-btn>
              <v-btn @click="getNextDocument(false)"> Next </v-btn>
            </template>



    </div>
  </div>
</template>

<script>

import BatchService from '@/services/batch.service'
import DoneAnnotationService from '@/services/done_annotation.service'
import QAForm from './QAForm.vue'
import Document from './Document'
import QA from './mixins/QA.js';
import Breadcrumbs from "./Breadcrumbs";

export default {
  name: 'QA',
  mixins: [
    QA,
  ],
  components: {
    QAForm,
    Document,
    Breadcrumbs,
  },
  props: {
    batchId: {
        type: String,
        required: true,
    },
  },
  data(){
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
    }
  },
  methods: {
    resetIndex(){
      this.annotation_index=0
    },
      skip(){
        this.getNextDocument(true)
      },
      getNextDocument(skip=false){
        let vm = this

        this.$store.commit('entities/CLEAR_ANNOTATED_ENTITIES')
        vm.annotations = null
        vm.tasks = null

        if (skip){
          this.skipped_document_ids.push(this.document.id)
        }

        BatchService.getBatchById(vm.batchId)
            .then(
                (res) => {
                    vm.project = res.data.project
                }
            )

        BatchService.getNextDocumentToQA(vm.batchId, this.skipped_document_ids, {
          only_non_reviewed_annotations: this.only_non_reviewed_annotations,
          index: this.annotation_index,
        })
          .then((response) => {
              vm.annotations = response.data.annotations
              vm.document = response.data.document
              vm.tasks = response.data.tasks
              vm.loaded = true
          })
          .catch((err) => {
              if (err.response.status == 404) {
                  this.noMore = true
                  this.document = null
              }
          })
        this.annotation_index++

      },
      taskAnnotations(task){
        return this.annotations.filter(a => a.task == task.id)
      },
      getFormForTask(task){
        return task.resourcetype+'Form'
      },
  },
  created(){
    this.done_annotation_service = new DoneAnnotationService()
    this.getNextDocument()
  },
}
</script>

<style lang="scss">


#qa-container {
    .v-btn--disabled.selected{
        border: 2px solid rgb(3, 169, 244);
        color: black !important;
    }
}

</style>

