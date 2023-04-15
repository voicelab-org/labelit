<template>
  <div>
    <p>RT seq. graph</p>
    <LineChart />
  </div>
</template>

<script>
import LineChart from '@/components/LineChart.vue';

export default {
  name: 'RealtimeSequenceGraph',
  components: {
    LineChart,
  },
  props: {
    sequence: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped></style>
