<template>
  <div>
    <p>Your annotations:</p>
    <LineChart :x="x" :y="y" />
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
  computed: {
    x() {
      return this.sequence.map(x => Math.round(x[0] * 100) / 100);
    },
    y() {
      return this.sequence.map(x => x[1]);
    },
  },
};
</script>

<style scoped></style>
