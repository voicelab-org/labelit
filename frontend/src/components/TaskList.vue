<template>
  <div>

    <div id="task-list-actions">
      <v-btn
          color="primary"
          dark
        >
          Add Task
        </v-btn>
    </div>

    <div id="tasks">

    <v-tabs>
      <v-tab @click="show_archived=false">
        Live
      </v-tab>
      <v-tab @click="show_archived=true">
        Archived
      </v-tab>
    </v-tabs>

    <v-simple-table>
      <thead>
        <tr>
          <th class="text-left">
            Name
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(task, i) in shown_tasks"
          :key="task.id"
          @click="goTo(task)"
        >
          <td>{{ task.name }}</td>

          <td>
            <TaskMenu v-model="shown_tasks[i]" />
          </td>
        </tr>
      </tbody>
    </v-simple-table>
  </div>

  </div>
</template>

<script>
import TaskService from '@/services/task.service'

import TaskMenu from '@/components/TaskMenu'

export default {
  name: 'task-list',
  components: {
    TaskMenu,
  },
  data(){
    return {
        tasks: [],
        show_archived: false,
    }
  },
  computed: {
    
    shown_tasks(){
      
      if (this.show_archived) {
        return this.tasks.filter(t => t.archived)
      } else {
        return this.tasks.filter(t => !t.archived)
      }
    },
    
  },
  created(){
    let vm = this;
    TaskService.getTaskList()
          .then(function(response){
               vm.tasks=response.data
           })
          .catch(error => console.log(error))
          .finally(() => vm.loading = false)
  },
  methods: {
    getLink(task){
        return "/task/"+task.id
    },
    goTo(task){
        this.$router.push('/task/'+task.id)
    },
  },
}
</script>

<style scoped lang="scss">

#tasks {
    .task {
        border: 1px solid lightgrey;
        border-bottom: none;
        padding: 15px 10px;
        cursor: pointer;
        &:hover{
            background: lightgrey;
            a {color: white !important;}
        }
    }
    a {
    color: rgb(4, 144, 174) !important;
    text-decoration: none;
    }

}


</style>
