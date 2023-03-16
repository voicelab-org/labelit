export const regions = {
  namespaced: true,
  state: {
    region_tasks: [
      /*// TEMP
        {
            id: 1,
            name: "IVR",
            color: "lightblue",
        },*/
    ],
    annotated_regions: [],
    annotation_enabled: true,
  },
  getters: {
    region_tasks(state) {
      return state.region_tasks;
    },
    annotated_regions(state) {
      return state.annotated_regions;
    },
    annotation_enabled(state) {
      return state.annotation_enabled;
    },
  },
  mutations: {
    CLEAR_ANNOTATED_REGIONS(state) {
      state.annotated_regions = [];
    },
    SET_ANNOTATED_REGIONS(state, regions) {
      state.annotated_regions = regions;
    },
    ADD_TASK(state, task) {
      if (
        state.region_tasks.find(t => {
          return t.id == task.id;
        })
      )
        return;
      state.region_tasks.push(task);
    },
    ADD_ANNOTATED_REGIONS(state, regions) {
      state.annotated_regions = state.annotated_regions.concat(regions);
    },
    RESET_ALL(state) {
      state.region_tasks = [];
      state.annotated_regions = [];
    },
    DISABLE_ANNOTATION(state) {
      state.annotation_enabled = false;
    },
    ENABLE_ANNOTATION(state) {
      state.annotation_enabled = true;
    },
  },
};
