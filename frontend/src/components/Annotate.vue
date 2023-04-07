<template>
  <div>
    <div v-if="moreToAnnotate" class="annotation-form">
      <span
        v-shortkey="['ctrl', 'alt', 'arrowup']"
        @shortkey.stop="browseTasks('left')"
      ></span>
      <span
        v-shortkey="['ctrl', 'alt', 'arrowdown']"
        @shortkey.stop="browseTasks('right')"
      ></span>

      <span v-shortkey="['ctrl', 'enter']" @shortkey="submit"></span>
      <div v-if="isUndoButtonShown && !reviewMode">
        <v-btn class="primary" @click="undo">UNDO</v-btn>
      </div>
      <div v-if="document && batch" id="doc-container">
        <Document
          :document="document"
          :project="batch.project"
          @loaded="startTiming"
        />
        <div v-if="batch.project.do_display_timer_time">
          Time: {{ time_display }}
        </div>
      </div>
      <div v-if="annotations" id="annotation-forms-t">
        <div v-if="tasksLoaded">
          <component
              :is="getAnnotationContainerForProject()"
              :annotations="annotations"
              :tasks="tasks"
              :submitting="submitting"
              @submitted="numTasksSubmitted++"
              :document="document"
              :project="batch.project"
          />
        </div>
      </div>
      <div v-if="annotations" id="actions-container">
        <v-btn color="primary" @click="submit()">SUBMIT</v-btn>
        <hotkey-guide />
      </div>
      <div
        v-if="isInactive && batch && !batch.project.do_display_timer_time"
        id="inactive"
      >
        <v-icon>mdi-pause</v-icon>
      </div>
    </div>
    <div v-else>No more to annotate.</div>
  </div>
</template>

<script>
import BatchService from '@/services/batch.service.js';
import TaskService from '@/services/task.service.js';
import QA from './mixins/QA.js';
import Timer from './mixins/Timer.js';
import Document from './Document.vue';
import HotkeyGuide from '@/components/HotkeyGuide.vue';

export default {
  name: 'Annotate',
  components: {
    Document,
    HotkeyGuide,
  },
  mixins: [QA, Timer],
  props: {
    batchId: {
      type: String,
      required: true,
    },
    reviewMode: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      batch: null,
      annotations: null,
      tasks: null,
      document: null,
      submitting: false,
      numTasksSubmitted: 0,
      moreToAnnotate: true,
      isUndoing: false,
      isFirstAnnotation: true,
      focus_index: 0,
    };
  },
  computed: {
    time_display() {
      return Math.round(this.time / 1000, 2);
    },
    tasksLoaded() {
      var vm = this;
      if (vm.annotations == null) return false;
      if (vm.tasks == null) return false;
      return vm.annotations.length == vm.tasks.length;
    },
    allSubmitted() {
      return this.numTasksSubmitted == this.tasks.length;
    },
    isUndoButtonShown() {
      return !this.isUndoing && !this.isFirstAnnotation;
    },
  },
  watch: {
    numTasksSubmitted(val) {
      let vm = this;
      if (!this.tasks) {
        return;
      } else {
        if (val == this.tasks.length && val !== 0) {
          vm.submitting = false;
          vm.getNextDocument();
        }
      }
    },
  },
  created() {
    this.getBatch();
    this.getNextDocument(true);

    this.$store.commit('entities/ENABLE_ANNOTATION');
  },
  methods: {
    getBatch() {
      BatchService.getBatchById(this.batchId)
        .then(response => {
          this.batch = response.data;
        })
        .catch(function (error) {
          console.error(error);
        });
    },
    undo() {
      let vm = this;
      vm.isUndoing = true;
      vm.annotations = null;
      vm.tasks = null;
      vm.submitting = false;
      vm.numTasksSubmitted = 0;
      BatchService.getDocumentToUndo(vm.batchId).then(response => {
        vm.annotations = response.data.annotations;
        vm.document = response.data.document;
        vm.getTasks();
      });
    },
    getNextDocument(isFirstAnnotation) {
      let vm = this;
      this.focus_index = 0;
      this.$store.commit('entities/CLEAR_ANNOTATED_ENTITIES');
      this.$store.commit('regions/CLEAR_ANNOTATED_REGIONS');
      this.$store.commit('player/SET_PLAYBACK_TIME', 0);
      vm.annotations = null;
      vm.tasks = null;
      vm.submitting = false;
      vm.numTasksSubmitted = 0;
      let getNext = vm.reviewMode
        ? BatchService.getNextDocumentToReview(vm.batchId)
        : BatchService.getBatchNextDocument(vm.batchId);
      getNext.then(function (response) {
        if (response.data === '') {
          vm.moreToAnnotate = false;
          return;
        }
        vm.annotations = response.data.annotations;
        vm.document = response.data.document;
        vm.getTasks();
      });
      vm.isUndoing = false;
      if (!isFirstAnnotation) {
        vm.isFirstAnnotation = false;
      }
    },
    submit() {
      this.submitting = true;
    },
    getTasks() {
      let vm = this;
      vm.annotations.forEach(function (annotation) {
        TaskService.getTaskById(annotation.task)
          .then(function (response) {
            if (vm.tasks == null) vm.tasks = [];
            vm.tasks.push(response.data);
          })
          .catch(err => console.error(err));
      });
    },
    getTaskForAnnotation(annotation) {
      var vm = this;
      return vm.tasks.filter(t => t.id == annotation.task)[0];
    },
    getFormForTask(task) {
      return task.resourcetype + 'Form';
    },
    handleSubmitError() {
      this.submitting = false;
      this.numTasksSubmitted = 0;
    },
    browseTasks(direction) {
      if (direction == 'right') {
        if (this.focus_index == this.annotations.length - 1) {
          this.focus_index = 0;
        } else {
          this.focus_index++;
        }
      }

      if (direction == 'left') {
        if (this.focus_index == 0) {
          this.focus_index = this.annotations.length - 1;
        } else {
          this.focus_index--;
        }
      }
    },
  },
};
</script>
<style scoped lang="scss">
#actions-container {
  margin-top: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.annotation-form {
  position: relative;
  padding: 10px 0;
  #inactive {
    display: flex;
    justify-content: space-around;
    align-items: center;

    background: black;
    opacity: 0.8;
    position: fixed;
    top: 0;
    height: 100%;
    z-index: 2000;
    width: calc(100% + 52px);
    left: -50px;
    > .v-icon {
      opacity: 1;
      color: white;
      font-size: 100px;
    }
  }
}
</style>
