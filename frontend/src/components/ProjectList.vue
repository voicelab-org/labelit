<template>
  <div>
    <div class="header">
      <h2 class="headline">Projects </h2>
      <div class="header-right">
        <project-creator v-if="isAdmin" @batchCreated="getProjects"/>
      </div>
    </div>
    <div id="projects">
      <v-tabs>
        <v-tab @click="show_archived=false">
          Live
        </v-tab>
        <v-tab @click="show_archived=true">
          Archived
        </v-tab>
      </v-tabs>
      <v-simple-table v-if="shown_projects.length">
        <thead>
        <tr>
          <th class="text-left">
            Name
          </th>
          <th class="text-left">
            Tasks
          </th>
        </tr>
        </thead>
        <tbody>
        <tr
            v-for="(project, i) in shown_projects"
            :key="project.id"
            @click="goTo(project)"
        >
          <td>{{ project.name }}</td>
          <td>{{ printProjectTasks(project.tasks) }}</td>
          <td>
            <ProjectMenu v-model="shown_projects[i]" />
          </td>
        </tr>
        </tbody>
      </v-simple-table>
      <div v-else>
        No projects
      </div>
    </div>
  </div>
</template>

<script>
import ProjectService from '@/services/project.service'
import ProjectMenu from '@/components/ProjectMenu'
import ProjectCreator from "./ProjectCreator";
import {mapGetters} from 'vuex'


export default {
  name: 'project-list',
  components: {
    ProjectMenu,
    ProjectCreator,
  },
  data() {
    return {
      projects: [],
      show_archived: false,
      loading: true,
    }
  },
  created() {
    this.getProjects()
  },
  methods: {
    getProjects(){
      this.loading = true
      ProjectService.getProjectList()
          .then( (response) => {
            this.projects = response.data
          })
          .catch(error => console.log(error))
          .finally(() => this.loading = false)
    },
    getLink(project) {
      return "/project/" + project.id
    },
    printProjectTasks(tasks) {
      return tasks.map(t => t.name).join(", ")
    },
    goTo(project) {
      this.$router.push('/project/' + project.id)
    },
  },
  computed: {
    ...mapGetters({
      isAdmin: 'auth/isAdmin',
    }),
    shown_projects() {
      if (this.show_archived) {
        return this.projects.filter(p => p.archived)
      } else {
        return this.projects.filter(p => !p.archived)
      }
    },
  },
}
</script>

<style scoped lang="scss">

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-right {
    display: flex;
  }
}

#projects {
  .project {
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
