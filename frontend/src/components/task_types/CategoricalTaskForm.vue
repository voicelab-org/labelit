<template>
  <div class="task-form-container">
    <TaskFormHeader :task="task" :read-only="readOnly" />
    <LabelSet
      v-model="selected_labels"
      :focused="focused"
      :read-only="readOnly"
      :labels="task.labels"
      :are-labels-exclusive="task.are_categories_exclusive"
    />
    <ValidationError :message="validationError" />
  </div>
</template>
<script>
import LabelSet from '@/components/LabelSet.vue';
import TaskForm from '@/components/mixins/TaskForm.vue';
import ValidationError from '@/components/ValidationError.vue';
import TaskFormHeader from '@/components/TaskFormHeader.vue';

export default {
  name: 'CategoricalTaskForm',
  components: {
    LabelSet,
    ValidationError,
    TaskFormHeader,
  },
  mixins: [TaskForm],
};
</script>

<style lang="scss">
.task-form-container {
  margin-bottom: 15px;
}
</style>
