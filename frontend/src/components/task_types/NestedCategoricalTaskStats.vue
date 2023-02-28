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
        <h5>Parent labels</h5>
        <BarChart
          :data="
            getBarChartData(
              stats.parent_label_distribution,
              'labels__nestedcategoricallabel__parent_label__name',
              'labels__nestedcategoricallabel__parent_label__color'
            )
          "
          :options="barchart_options"
        />
        <h5>Children labels</h5>
        <BarChart
          :data="getBarChartData(stats.children_label_distribution)"
          :options="barchart_options"
        />
      </div>
    </div>
  </div>
</template>

<script>
import TaskStats from "@/components/mixins/TaskStats.js";
import BarChart from "@/components/BarChart";

export default {
  name: "NestedCategoricalTaskStats",
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
    getBarChartData(distribution, name_prop, color_prop) {
      //labels__name, labels__color
      if (!name_prop) name_prop = "labels__name";
      if (!color_prop) color_prop = "labels__color";
      let data = {};
      data.labels = distribution.map((d) => d[name_prop]);
      data.datasets = [
        {
          data: distribution.map((d) => d.count),
          borderWidth: 2,
          barThickness: 60,
          backgroundColor: distribution.map((d) => d[color_prop]),
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
