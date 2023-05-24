<template>
  <LineChartjs :data="chartData" />
</template>

<script>
// DataPage.vue
import { Line } from 'vue-chartjs';

const LineChartjs = Line;
import {
  Chart,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from 'chart.js';

Chart.register(
  Title,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale
);

export default {
  name: 'LineChart',
  components: { LineChartjs },
  props: {
    x: {
      type: Array,
      default: [1, 2, 3],
    },
    y: {
      type: Array,
      default: [40, 20, 12],
    },
  },
  data() {
    return {
      chartData: {
        labels: this.x,
        datasets: [
          {
            label: 'Annotations',
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
            data: this.y,
          },
        ],
      },
    };
  },
};
</script>
