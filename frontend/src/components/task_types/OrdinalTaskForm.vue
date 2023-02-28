<template>
  <div class="task-form-container">
    <TaskFormHeader :task="task" :read-only="readOnly" />
    <LabelSet
      :read-only="readOnly"
      :labels="task.labels"
      v-model="selected_labels"
      :value-field="'index'"
    />
    <ValidationError :message="validationError" />
  </div>
</template>
<script>
import LabelSet from "@/components/LabelSet";
import TaskForm from "@/components/mixins/TaskForm";
import ValidationError from "@/components/ValidationError";
import TaskFormHeader from "@/components/TaskFormHeader";

export default {
  name: "ordinal-task-form",
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
