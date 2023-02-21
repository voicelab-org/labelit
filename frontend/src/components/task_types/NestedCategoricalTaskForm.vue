<template>
  <div class="task-form-container">
    <TaskFormHeader :task="task" :read-only="readOnly" />
    <NestedLabelSet
      :focused="focused"
      :read-only="readOnly"
      :labels="task.labels"
      v-model="selected_labels"
      :single-select="task.single_select"
    />
    <ValidationError :message="validationError" />
  </div>
</template>
<script>
import NestedLabelSet from "@/components/NestedLabelSet";
import TaskForm from "@/components/mixins/TaskForm";
import ValidationError from "@/components/ValidationError";
import TaskFormHeader from "@/components/TaskFormHeader";

export default {
  name: "categorical-task-form",
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
