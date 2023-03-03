<template>
  <div>
    <div v-if="task">
      <component
        :is="annotationFormComponentName"
        :annotation="annotation"
        :task="task"
      />
    </div>
  </div>
</template>
<script>
import TaskService from '@/services/task.service';

export default {
  name: 'AnnotationForm',
  props: {
    annotation: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      task: null,
    };
  },
  computed: {
    annotationFormComponentName() {
      return this.task.resourcetype + 'Form';
    },
  },
  created() {
    let vm = this;
    TaskService.getTaskById(annotation.task)
      .then(function (response) {
        vm.task = response.data;
      })
      .catch(error => console.error(error));
  },
};
</script>
