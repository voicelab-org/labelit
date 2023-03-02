import AnnotationService from '@/services/annotation.service.js';

export default {
  name: 'TaskForm',
  mixins: [],
  props: {
    submitting: {
      type: Boolean,
      required: true,
    },
    annotation: {
      type: Object,
      required: true,
    },
    task: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
    reviewMode: {
      type: Boolean,
      default: false,
    },
    validationError: {
      type: String,
      default: '',
    },
    time: {
      type: Number,
    },
    document: {
      type: Object,
      required: true,
    },
    focused: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      selected_labels: [],
      selected_labels_loaded: false,
      isMixinWatcherActive: true,
    };
  },
  created() {
    if (this.isMixinWatcherActive) {
      var vm = this;
      vm.selected_labels = vm.annotation.labels.map(function (id) {
        return vm.task.labels.filter(label => label.id == id)[0];
      });
    }
  },
  watch: {
    selected_labels: {
      deep: true,
      handler(val) {
        if (!this.isMixinWatcherActive) {
          return;
        }
        let vm = this;

        if (!vm.selected_labels_loaded) {
          vm.selected_labels_loaded = true;
          return;
        }
        var editedAnnotation = {};
        Object.assign(editedAnnotation, vm.annotation);

        editedAnnotation['labels'] = val.map(l => l.id);

        AnnotationService.updateAnnotation(vm.annotation.id, editedAnnotation)
          .then(() => {
            this.validationError = '';
          })
          .catch(error => {
            this.validationError = error.response.data.non_field_errors[0];
          });
      },
    },
    submitting: function () {
      if (!this.isMixinWatcherActive) {
        return;
      }

      let vm = this;
      if (vm.submitting) {
        var editedAnnotation = {};
        Object.assign(editedAnnotation, vm.annotation);
        editedAnnotation['is_done'] = true;
        editedAnnotation['labels'] = vm.selected_labels.map(l => l.id);

        editedAnnotation['time'] = vm.time;
        if (editedAnnotation.has_qa_invalidated) {
          editedAnnotation.is_resubmitted = true;
        }
        AnnotationService.updateAnnotation(vm.annotation.id, editedAnnotation)
          .then(() => {
            this.validationError = '';
            vm.$emit('submitted');
          })
          .catch(error => {
            this.validationError = error.response.data.non_field_errors[0];
            vm.$emit('submiterror');
          });
      }
    },
  },
};
