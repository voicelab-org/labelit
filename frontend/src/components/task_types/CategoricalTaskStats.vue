<template>
  <div class="task-stats">
    <h4>Stats for task: {{ task.name }}</h4>
    <div v-if="stats">
      <table class="stats-table" v-if="stats.agreement">
        <tr>
          <td class="left">{{ stats.agreement.metric }}</td>
          <td>{{ stats.agreement.value }}</td>
        </tr>
      </table>
      <div v-if="stats" class="barchart-container">
        <h5>All annotators</h5>

        <BarChart
          :data="getBarChartData(stats.annotation_distribution)"
          :options="barchart_options"
        />
        <div
          v-for="annotator_distribution in stats.per_annotator_distributions"
          :key="annotator_distribution[0].annotator_last_name"
        >
          <h5>
            Annotated by: {{ annotator_distribution[0].annotator_first_name }}
            {{ annotator_distribution[0].annotator_last_name }}
          </h5>
          <BarChart
            :data="getBarChartData(annotator_distribution)"
            :options="barchart_options"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TaskStats from "@/components/mixins/TaskStats.js";
import BarChart from "@/components/BarChart";

export default {
  name: "CategoricalTaskStats",
  mixins: [TaskStats],
  components: {
    BarChart,
  },
  computed: {
    barchart_options() {
      return {
        maintainAspectRatio: false,

        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                stepSize: 1,
              },
            },
          ],
        },
        legend: {
          display: false,
        },
      };
    },
  },
  methods: {
    getBarChartData(distribution) {
      let data = {};
      data.labels = distribution.map((d) => d.labels__name);
      data.datasets = [
        {
          data: distribution.map((d) => d.count),
          borderWidth: 2,
          barThickness: 60,
          backgroundColor: distribution.map((d) => d.labels__color),
        },
      ];
      return data;
    },
  },
};
</script>

<style lang="scss">
h5 {
  margin-top: 15px;
  margin-bottom: 10px;
}
</style>
