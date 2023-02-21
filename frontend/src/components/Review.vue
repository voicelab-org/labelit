<template>
  <div id="review-container">
    <Annotate :batch-id="batchId" :review-mode="true" />
  </div>
</template>

<script>
import Annotate from "./Annotate.vue";

export default {
  name: "Review",
  props: {
    batchId: {
      type: String,
      required: true,
    },
  },
  components: {
    Annotate,
  },
};
</script>

<style lang="scss"></style>
