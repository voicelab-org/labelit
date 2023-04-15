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
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

Chart.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default {
  name: 'LineChart',
  components: { LineChartjs },
  data() {
    return {
      chartData: {
        labels: ['1', '2', '3'],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [40, 20, 12],
          },
        ],
      },
    };
  },
};
</script>
