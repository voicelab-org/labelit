<template>
  <div id="review-container">
    <Annotate :batch-id="batchId" :review-mode="true" />
  </div>
</template>

<script>
import Annotate from './Annotate.vue';

export default {
  name: 'Review',
  components: {
    Annotate,
  },
  props: {
    batchId: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss"></style>
