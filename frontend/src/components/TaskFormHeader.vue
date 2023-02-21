<template>
  <div>
    <div v-if="task && !readOnly" class="task-header">
      <div>
        <b>{{ task.name }}</b>
        <Guidelines :task="task" />
      </div>
      <img v-if="task.image" :src="task.image" />
    </div>
  </div>
</template>

<script>
import Guidelines from "./Guidelines";

export default {
  name: "TaskFormHeader",
  components: { Guidelines },
  props: {
    task: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
