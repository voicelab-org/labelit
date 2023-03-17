import Vue from 'vue';
import Vuex from 'vuex';

import { auth } from './auth.module.js';
import { blueFilter } from './blue-filter.module.js';
import { entities } from './entities.module.js';
import { player } from './player.module.js';
import { regions } from './audioregions.module.js';
import { snackbar } from './snackbar.module.js';
import { task } from './task.module.js';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    blueFilter,
    entities,
    player,
    regions,
    snackbar,
    task,
  },
});
