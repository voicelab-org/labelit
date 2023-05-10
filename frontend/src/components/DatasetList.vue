<template>
  <div id="datasets">
    <div class="d-flex align-center justify-space-between">
      <h2 class="headline">{{ $t('Datasets') }}</h2>
      <div class="actions">
        <DatasetUploader @new-dataset-imported="getDatasets()" />
      </div>
    </div>
    <div class="mt-12">
      <div v-if="loading" class="d-flex justify-center">
        <v-progress-circular
          color="blue-grey"
          indeterminate
        ></v-progress-circular>
      </div>
      <div v-else>
        <div v-if="datasets.length === 0" class="mt-12 text-center">
          {{ $t('No dataset imported yet') }}
        </div>
        <v-simple-table v-else>
          <thead>
            <tr>
              <th class="text-left">{{ $t('Name') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="dataset in datasets" :key="dataset.id" class="no-click">
              <td>{{ dataset.name }}</td>
            </tr>
          </tbody>
        </v-simple-table>
      </div>
    </div>
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
      loading: true,
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
