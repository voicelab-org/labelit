<template>
  <div>
    <div class="header">
      <h2 class="headline" v-if="project">Project: {{ project.name }} </h2>
      <div class="header-right">
        <v-btn @click="exportProject"> Export</v-btn>
        <batch-create v-if="isAdmin" :projectId="projectId" @batchCreated="updateListToggle=!updateListToggle"/>
      </div>
    </div>
    <div
        v-if="project_with_stats"
        class="d-flex flex-row justify-space-between"
    >
          <div># documents annotated: {{project_with_stats.num_done_documents}}</div>
          <div>Target (# documents to annotate): {{project_with_stats.target_num_documents}} </div>
          <div>Target date: {{project_with_stats.target_deadline}} </div>
          <v-progress-linear
          v-if="project_with_stats.target_num_documents && project_with_stats.num_done_documents"
          :value="Math.round(
            100 * project_with_stats.num_done_documents / project_with_stats.target_num_documents
            )"
            height="25"
        ></v-progress-linear>
        <p v-if="project_with_stats.description">
          <b>Description: </b><br>
          <span style="white-space: pre;">{{project_with_stats.description}}</span>
        </p>
      </div>


    <v-tabs>
      <v-tab @click="show_batch_list=true">
        Batches
      </v-tab>
      <v-tab  @click="show_batch_list=false">
        Stats
      </v-tab>
    </v-tabs>
    <router-view />

    <template v-if="project && show_batch_list">
      <BatchList :project="project" :update="updateListToggle"/>
    </template>
    <template v-if="!show_batch_list && project">
      <Stats :project-id="project.id" />
    </template>
  </div>
</template>

<script>

import ProjectService from '@/services/project.service'
import BatchCreate from '@/components/BatchCreate'
import Stats from '@/components/Stats'
import {mapGetters} from 'vuex'

import BatchList from '@/components/BatchList'

export default {
  name: 'project',
  components: {BatchCreate, BatchList, Stats},
  props: {
    projectId: {
      type: String,
      required: true
    },
  },
  data() {
    return {
      batches: [],
      project: null,
      loading: true,
      show_archived: false,
      show_batch_list: true,
      updateListToggle: true,
      project_with_stats: null,
    }
  },
  computed: {
    ...mapGetters({
      isAdmin: 'auth/isAdmin',
    }),

  },
  created() {

    let vm = this
    ProjectService.getProjectById(vm.projectId)
        .then(function (response) {
          vm.project = response.data
          //vm.$store.commit('task/SET_TASK_LIST', response.data.tasks)
          vm.loading = false
        })
        .catch(error => console.log(error))

    ProjectService.getProjectWithStats(vm.projectId)
        .then(function (response) {
          vm.project_with_stats = response.data
        })
        .catch(error => console.log(error))
  },
  methods: {
    exportProject() {
      //ProjectService.exportProject(this.projectId).then(
      ProjectService.downloadExportedProject(this.projectId)/*.then(
          (res) => {
            console.log("&res: ", res.data)
          }
      )*/
    },
    getLink(batch) {
      return "/batch/" + batch.id
    },
  },
}
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

