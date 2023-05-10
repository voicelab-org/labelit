<template>
  <div>
    <v-tabs>
      <v-tab @click="show_archived = false">{{$t('Live batches')}}</v-tab>
      <v-tab @click="show_archived = true">{{$t('Archived batches')}}</v-tab>
    </v-tabs>

    <v-simple-table v-if="shown_batches.length && !loading">
      <thead>
        <tr>
          <th class="text-left">{{$t('Name')}}</th>
          <th class="text-left actions-table-column"></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(batch, i) in shown_batches"
          :key="batch.id"
          @click="goTo(batch)"
        >
          <td>{{ batch.name }}</td>
          <td v-if="isAdmin">
            <BatchMenu v-model="shown_batches[i]" />
          </td>
        </tr>
      </tbody>
    </v-simple-table>

    <div v-if="!loading && !shown_batches.length">
      {{$t('No batches')}}
    </div>
    <div v-if="loading" class="loading">
      <v-progress-circular
        color="blue-grey"
        indeterminate
      ></v-progress-circular>
    </div>
  </div>
</template>

<script>
import BatchService from '@/services/batch.service.js';
import ProjectService from '@/services/project.service.js';

import { mapGetters } from 'vuex';

import BatchMenu from '@/components/BatchMenu.vue';

export default {
  name: 'BatchList',
  components: { BatchMenu },
  props: {
    project: {
      type: Object,
      required: true,
    },
    update: {
      type: Boolean,
    },
  },
  data() {
    return {
      batches: [],
      loading: true,
      show_archived: false,
    };
  },
  computed: {
    ...mapGetters({
      isAdmin: 'auth/isAdmin',
    }),
    shown_batches() {
      if (this.show_archived) {
        return this.batches.filter(b => b.archived);
      } else {
        return this.batches.filter(b => !b.archived);
      }
    },
  },

  watch: {
    update() {
      this.getBatchList();
    },
  },
  created() {
    this.getBatchList();
  },
  methods: {
    exportProject() {
      ProjectService.downloadExportedProject(this.projectId);
    },
    getLink(batch) {
      return '/batch/' + batch.id;
    },
    goTo(batch) {
      this.$router.push('/batch/' + batch.id, () => {});
    },
    getBatchList() {
      let vm = this;
      vm.loading = true;
      BatchService.getBatchList({
        project_id: vm.project.id,
      })
        .then(function (response) {
          vm.batches = response.data;
          vm.loading = false;
        })
        .catch(error => console.error(error));
    },
  },
};
</script>

<style lang="scss" scoped>
.loading {
  margin: 10px 0;
  display: flex;
  justify-content: center;
}
</style>
