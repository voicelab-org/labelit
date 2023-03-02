<template>
  <div id="datasets">
    <div class="actions">
      <DatasetUploader @imported="getDatasets()" />
    </div>
    <v-simple-table>
      <thead>
        <tr>
          <th class="text-left">Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="dataset in datasets" :key="dataset.id" class="no-click">
          <td>{{ dataset.name }}</td>
        </tr>
      </tbody>
    </v-simple-table>
  </div>
</template>

<script>
import DatasetService from '@/services/dataset.service.js';

import DatasetUploader from '@/components/DatasetUploader.vue';

export default {
  name: 'DatasetList',
  components: {
    DatasetUploader,
  },
  data() {
    return {
      datasets: [],
    };
  },
  created() {
    this.getDatasets();
  },
  methods: {
    getDatasets() {
      DatasetService.getDatasetList()
        .then(response => {
          this.datasets = response.data;
        })
        .catch(error => console.error(error))
        .finally(() => (this.loading = false));
    },
    getLink(dataset) {
      return '/dataset/' + dataset.id;
    },
    printDatasetTasks(tasks) {
      return tasks.map(t => t.name).join(', ');
    },
    goTo(dataset) {
      this.$router.push('/dataset/' + dataset.id);
    },
  },
};
</script>

<style scoped lang="scss">
#datasets {
  .dataset {
    border: 1px solid lightgrey;
    border-bottom: none;
    padding: 15px 10px;
    cursor: pointer;

    &:hover {
      background: lightgrey;

      a {
        color: white !important;
      }
    }
  }

  a {
    color: rgb(4, 144, 174) !important;
    text-decoration: none;
  }
}
</style>
