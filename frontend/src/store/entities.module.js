export const entities = {
  namespaced: true,
  state: {
    entity_tasks: [
      // TEMP
      /*{
          id: 1,
          name: "Task 1",
          labels: [
              {"id":1,"name":"Véhicule","prefix_key":null,"suffix_key":"0","background_color":"#FF8000","text_color":"#ffffff"},
              {"id":2,"name":"Numéro de sociétaire","prefix_key":null,"suffix_key":"1","background_color":"#00FFD7","text_color":"#ffffff"},
              {"id":3,"name":"Immatriculation","prefix_key":null,"suffix_key":"2","background_color":"#D0FF00","text_color":"#ffffff"},
              {"id":4,"name":"Lieu","prefix_key":null,"suffix_key":"3","background_color":"#5E00FF","text_color":"#ffffff"},
              {"id":5,"name":"Adresse","prefix_key":null,"suffix_key":"4","background_color":"#1B5E20","text_color":"#ffffff"},
              {"id":6,"name":"Nom","prefix_key":null,"suffix_key":"5","background_color":"#607D8B","text_color":"#ffffff"},
              {"id":7,"name":"Numéro de tel.","prefix_key":null,"suffix_key":"6","background_color":"#FDD835","text_color":"#ffffff"},
              {"id":8,"name":"Adresse e-mail","prefix_key":null,"suffix_key":"7","background_color":"#1E88E5","text_color":"#ffffff"}
          ],
        },*/
      // END TEMP
    ],
    annotated_entities: [],
    annotation_enabled: true,
  },
  getters: {
    entity_tasks(state) {
      return state.entity_tasks;
    },
    annotated_entities(state) {
      return state.annotated_entities;
    },
    annotation_enabled(state) {
      return state.annotation_enabled;
    },
  },
  mutations: {
    CLEAR_ANNOTATED_ENTITIES(state) {
      state.annotated_entities = [];
    },
    SET_ANNOTATED_ENTITIES(state, entities) {
      state.annotated_entities = entities;
    },
    ADD_TASK(state, task) {
      if (
        state.entity_tasks.find(t => {
          return t.id == task.id;
        })
      )
        return;
      state.entity_tasks.push(task);
    },
    ADD_ANNOTATED_ENTITIES(state, entities) {
      state.annotated_entities = state.annotated_entities.concat(entities);
    },
    RESET_ALL(state) {
      state.entity_tasks = [];
      state.annotated_entities = [];
    },
    DISABLE_ANNOTATION(state) {
      state.annotation_enabled = false;
    },
    ENABLE_ANNOTATION(state) {
      state.annotation_enabled = true;
    },
  },
};
