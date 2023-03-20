<template>
  <div class="task-form-container">
    <TaskFormHeader :task="task" :read-only="readOnly" />
    <NestedLabelSet
      v-model="selected_labels"
      :focused="focused"
      :read-only="readOnly"
      :labels="task.labels"
      :single-select="task.single_select"
    />
    <ValidationError :message="validationError" />
  </div>
</template>
<script>
import NestedLabelSet from '@/components/NestedLabelSet.vue';
import TaskForm from '@/components/mixins/TaskForm.js';
import ValidationError from '@/components/ValidationError.vue';
import TaskFormHeader from '@/components/TaskFormHeader.vue';

export default {
  name: 'CategoricalTaskForm',
  components: {
    NestedLabelSet,
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
