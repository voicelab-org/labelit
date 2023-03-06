<template>
  <div class="task-form-container">
    <TaskFormHeader :task="task" :read-only="readOnly" />
    <LabelSet
      v-model="selected_labels"
      :read-only="readOnly"
      :labels="task.labels"
      :value-field="'index'"
    />
    <ValidationError :message="validationError" />
  </div>
</template>
<script>
import LabelSet from '@/components/LabelSet.vue';
import TaskForm from '@/components/mixins/TaskForm.js';
import ValidationError from '@/components/ValidationError.vue';
import TaskFormHeader from '@/components/TaskFormHeader.vue';

export default {
  name: 'OrdinalTaskForm',
  components: {
    LabelSet,
    ValidationError,
    TaskFormHeader,
  },
  mixins: [TaskForm],
};
</script>

<style>
.task-form-container {
  margin-bottom: 15px;
}
</style>
