import ProjectTaskService from "@/services/project_task.service";
import Project_taskService from "@/services/project_task.service";

export default {
  name: 'AnnotationContainer',
  props: {
    document: {
      type: Object,
      required: true
    },
    project: {
      type: Object,
      required: true,
    },
    annotations: {
      type: Array,
      required: true,
    },
    tasks: {
      type: Array,
      required: true,
    },
    time: {
      type: Number,
    },
    submitting: {
      type: Boolean,
      required: true,
    },
    reviewMode: {
      type: Boolean,
    },
  },
  created(){
    console.log("AnnotationContainer.js created()")
    Project_taskService.list({project: this.project.id}).then(
        (res) => {
          console.log("res: ", res.data)
        }
    )
  },
  data(){
    return {}
  },
  methods: {
    getFormForTask(task) {
      return task.resourcetype + 'Form';
    },
    getTaskForAnnotation(annotation) {
      var vm = this;
      return vm.tasks.filter(t => t.id == annotation.task)[0];
    },
    getAnnotationClasses(a, is_focused) {
      return {
        annotation: true,
        validated: a.has_qa_validated,
        invalidated: a.has_qa_invalidated,
        resubmitted: a.is_resubmitted,
        is_focused: is_focused,
      };
    },
  },
};
