<template>
  <div>
    <div id="tasks">
      <div class="header">
        <h2 class="headline">{{$t('Tasks')}}</h2>
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
        <v-tab @click="show_archived = false">{{$t('Live tasks')}}</v-tab>
        <v-tab @click="show_archived = true">{{$t('Archived task')}}</v-tab>
      </v-tabs>
      <div v-if="loading" class="d-flex justify-center mt-12">
        <v-progress-circular
          color="blue-grey"
          indeterminate
        ></v-progress-circular>
      </div>
      <div v-else>
        <v-simple-table>
          <thead>
            <tr>
              <th class="text-left">{{ $t('Name') }}</th>
              <th class="text-left">{{ $t('Type')}}</th>
              <th class="text-left actions-table-column"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(task, i) in shown_tasks"
              :key="task.id"
              @click="goTo(task)"
            >
              <td>{{ task.name }}</td>
              <td>{{ task.resourcetype }}</td>
              <td v-if="isAdmin">
                <TaskMenu v-model="shown_tasks[i]" @edit="showEdit" />
              </td>
            </tr>
          </tbody>
        </v-simple-table>
      </div>
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
      loading: true,
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
