<template>
  <div>
    <div class="d-flex justify-space-between align-center">
      <div class="d-flex align-center">
        <v-btn icon @click="$router.push('/projects')">
          <v-icon> mdi-arrow-left </v-icon>
        </v-btn>
        <h2 v-if="project" class="headline">Project: {{ project.name }}</h2>
      </div>
      <div class="d-flex">
        <v-btn @click="exportProject"> Export</v-btn>
        <batch-create
          v-if="isAdmin"
          :project-id="projectId"
          @batchCreated="updateListToggle = !updateListToggle"
        />
      </div>
    </div>
    <div class="d-flex justify-center mt-12">
      <v-progress-linear
        :value="
          project_with_stats === null
            ? 0
            : Math.round(
                (100 * project_with_stats.num_done_documents) /
                  project_with_stats.target_num_documents
              )
        "
        height="30"
      >
        <template #default="{ value }">
          <strong>{{ Math.ceil(value) }}%&nbsp;&nbsp;</strong>
          <small>
            ({{ project_with_stats?.num_done_documents }}/{{
              project_with_stats?.target_num_documents
            }}
            documents)
          </small>
        </template>
      </v-progress-linear>
    </div>
    <v-tabs v-model="currentTab" class="mt-12">
      <v-tab v-for="tab in tabs" :key="tab">
        {{ tab }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="currentTab">
      <v-tab-item key="Batches">
        <div v-if="project">
          <BatchList :project="project" :update="updateListToggle" />
        </div>
      </v-tab-item>
      <v-tab-item key="Information">
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Created on</v-list-item-title>
            <v-list-item-subtitle>{{
              project?.created_at
            }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Created by</v-list-item-title>
            <v-list-item-subtitle
              >{{ project?.created_by.first_name }}
              {{ project?.created_by.last_name }}</v-list-item-subtitle
            >
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Last modified</v-list-item-title>
            <v-list-item-subtitle>{{
              project?.updated_at
            }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="project_with_stats?.target_deadline">
          <v-list-item-content>
            <v-list-item-title>Target date</v-list-item-title>
            <v-list-item-subtitle>{{
              project_with_stats.target_deadline
            }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content v-if="project_with_stats?.description">
            <v-list-item-title>Description</v-list-item-title>
            <v-list-item-subtitle>{{
              project_with_stats.description
            }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-tab-item>
      <v-tab-item key="Statistics">
        <div v-if="project">
          <Stats :project-id="project.id" />
        </div>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import ProjectService from '@/services/project.service.js';
import BatchCreate from '@/components/BatchCreate.vue';
import Stats from '@/components/Stats.vue';
import { mapGetters } from 'vuex';

import BatchList from '@/components/BatchList.vue';

export default {
  name: 'Project',
  components: { BatchCreate, BatchList, Stats },
  props: {
    projectId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      batches: [],
      project: null,
      loading: true,
      currentTab: 'Batches',
      tabs: ['Batches', 'Informations', 'Statististics'],
      updateListToggle: true,
      project_with_stats: null,
    };
  },
  computed: {
    ...mapGetters({
      isAdmin: 'auth/isAdmin',
    }),
  },
  created() {
    let vm = this;
    ProjectService.getProjectById(vm.projectId)
      .then(function (response) {
        vm.project = response.data;
        //vm.$store.commit('task/SET_TASK_LIST', response.data.tasks)
        vm.loading = false;
      })
      .catch(error => console.error(error));

    ProjectService.getProjectWithStats(vm.projectId)
      .then(function (response) {
        vm.project_with_stats = response.data;
      })
      .catch(error => console.error(error));
  },
  methods: {
    exportProject() {
      ProjectService.downloadExportedProject(this.projectId);
    },
    getLink(batch) {
      return '/batch/' + batch.id;
    },
  },
};
</script>

<style lang="scss" scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-right {
    display: flex;
  }
}

.loading {
  margin: 10px 0;
  display: flex;
  justify-content: center;
}
</style>
