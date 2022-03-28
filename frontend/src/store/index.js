import Vue from "vue";
import Vuex from "vuex";

import { auth } from "./auth.module";
import { task } from "./task.module";
import { player } from "./player.module";

import { entities } from "./entities.module";


Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    task,
    player,
    entities,
  }
});
