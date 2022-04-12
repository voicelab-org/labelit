import TaskService from '@/services/task.service'

export const task = {
  namespaced: true,
  state: {
    taskList : null,
  },
  actions: {
    getTaskList({ commit }, projectId) {
      return TaskService.getTaskList({ project_id: projectId})
        .then((res) => {
          commit('SET_TASK_LIST', res.data)
          .catch(function(error){
            console.log(error)
          })
        })
    },
  },
  mutations: {
    SET_TASK_LIST(state, taskList) {
      state.taskList = taskList
    },
  }
};
