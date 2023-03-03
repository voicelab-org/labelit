<template>
  <div>
    <div id="tasks">
      <div class="header">
        <h2 class="headline">Tasks</h2>
        <div class="header-right">
          <task-manager v-if="isAdmin" @changed="getTasks" />
          <task-manager
            v-if="isAdmin"
            v-model="show_edit_task"
            :task="edited_task"
            @changed="getTasks"
          />
        </div>
      </div>
      <v-tabs>
        <v-tab @click="show_archived = false"> Live </v-tab>
        <v-tab @click="show_archived = true"> Archived </v-tab>
      </v-tabs>

      <v-simple-table>
        <thead>
          <tr>
            <th class="text-left">Name</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(task, i) in shown_tasks"
            :key="task.id"
            @click="goTo(task)"
          >
            <td>{{ task.name }} ({{ task.resourcetype }})</td>
            <td>
              <TaskMenu v-model="shown_tasks[i]" @edit="showEdit" />
            </td>
          </tr>
        </tbody>
      </v-simple-table>
    </div>
  </div>
</template>

<script>
import TaskService from '@/services/task.service.js';
import { mapGetters } from 'vuex';
import TaskMenu from '@/components/TaskMenu.vue';
import TaskManager from './TaskManager.vue';

export default {
  name: 'TaskList',
  components: {
    TaskMenu,
    TaskManager,
  },
  data() {
    return {
      tasks: [],
      show_archived: false,
      edited_task: { some: 'task' },
      show_edit_task: false,
    };
  },
  computed: {
    ...mapGetters({
      isAdmin: 'auth/isAdmin',
    }),
    shown_tasks() {
      if (this.show_archived) {
        var tasks = this.tasks.filter(t => t.archived);
      } else {
        tasks = this.tasks.filter(t => !t.archived);
      }
      return tasks.sort((a, b) => (a.created_at < b.created_at ? 1 : -1));
    },
  },
  created() {
    this.getTasks();
  },
  methods: {
    showEdit(task) {
      this.edited_task = task;
      this.show_edit_task = true;
    },
    getTasks() {
      TaskService.getTaskList()
        .then(response => {
          this.tasks = response.data;
          this.edited_task = { some: 'task' };
        })
        .catch(error => console.error(error))
        .finally(() => (this.loading = false));
    },
    getLink(task) {
      return '/task/' + task.id;
    },
    goTo(task) {
      this.$router.push('/task/' + task.id);
    },
  },
};
</script>

<style scoped lang="scss">
#tasks {
  .task {
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-right {
    display: flex;
  }
}
</style>
