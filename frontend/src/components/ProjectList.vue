<template>
  <div>
    <div class="header">
      <h2 class="headline">
        {{$t('Projects')}}
      </h2>
      <div class="header-right">
        <project-manager v-if="isAdmin" @changed="getProjects" />
        <project-manager
          v-model="show_edit_project"
          :project="edited_project"
          @changed="projectEdited"
        />
      </div>
    </div>
    <div id="projects">
      <v-tabs>
        <v-tab @click="show_archived = false">
          {{$t('Live projects')}}
        </v-tab>
        <v-tab @click="show_archived = true">
          {{$t('Archived projects')}}
        </v-tab>
      </v-tabs>
      <div v-if="loading" class="d-flex justify-center mt-12">
        <v-progress-circular
          color="blue-grey"
          indeterminate
        ></v-progress-circular>
      </div>
      <div v-else>
        <v-simple-table v-if="shown_projects.length">
          <thead>
            <tr>
              <th class="text-left">Project name</th>
              <th class="text-left">Tasks</th>
              <th class="text-left actions-table-column"></th>
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
              <td v-if="isAdmin">
                <ProjectMenu v-model="shown_projects[i]" @edit="showEdit" />
              </td>
            </tr>
          </tbody>
        </v-simple-table>
        <div class="text-center" v-else>No projects yet...</div>
      </div>
    </div>
  </div>
</template>

<script>
import ProjectService from '@/services/project.service.js';
import ProjectMenu from '@/components/ProjectMenu.vue';
import ProjectManager from './ProjectManager.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'ProjectList',
  components: {
    ProjectMenu,
    ProjectManager,
  },
  data() {
    return {
      projects: [],
      show_archived: false,
      loading: true,
      edited_project: { some: 'project' },
      show_edit_project: false,
    };
  },
  created() {
    this.getProjects();
  },
  methods: {
    projectEdited() {
      this.edited_project = { some: 'project' };
      this.getProjects();
    },
    showEdit(project) {
      this.edited_project = project;
      this.show_edit_project = true;
    },
    getProjects() {
      this.loading = true;
      ProjectService.getProjectList()
        .then(response => {
          this.projects = response.data;
        })
        .catch(error => console.error(error))
        .finally(() => (this.loading = false));
    },
    getLink(project) {
      return '/project/' + project.id;
    },
    printProjectTasks(tasks) {
      return tasks.map(t => t.name).join(', ');
    },
    goTo(project) {
      this.$router.push('/project/' + project.id);
    },
  },
  computed: {
    ...mapGetters({
      isAdmin: 'auth/isAdmin',
    }),
    shown_projects() {
      if (this.show_archived) {
        var projects = this.projects.filter(p => p.archived);
      } else {
        projects = this.projects.filter(p => !p.archived);
      }
      return projects.sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
    },
  },
};
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
