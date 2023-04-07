import Vue from 'vue';
import router from './router';
import store from './store/index.js';
import App from './App.vue';

import i18n from '@/plugins/i18n';
import VJsf from '@koumoul/vjsf/lib/VJsf.js';
import '@koumoul/vjsf/lib/VJsf.css';
import draggable from 'vuedraggable';

import upperFirst from 'lodash/upperFirst';
import camelCase from 'lodash/camelCase';

import VueUploadComponent from 'vue-upload-component';
Vue.component('FileUpload', VueUploadComponent);

Vue.component('VJsf', VJsf);
Vue.component('draggable', draggable);

import interceptorsSetup from '@/services/interceptors';
interceptorsSetup();

import vuetify from './plugins/vuetify';

import VueShortkey from 'vue-shortkey';
Vue.use(VueShortkey);

import VueScrollTo from 'vue-scrollto';
Vue.use(VueScrollTo);

// We must register these components because they will be dynamically called

const files = import.meta.globEager('@/components/task_types/*.vue');

for (const fileName in files) {
  // Get PascalCase name of component
  const componentName = upperFirst(
    camelCase(
      // Gets the file name regardless of folder depth
      fileName
        .split('/')
        .pop()
        .replace(/\.\w+$/, '')
    )
  );

  // Register component
  Vue.component(componentName, files[fileName].default);
}

Vue.config.productionTip = false;

new Vue({
  i18n,
  vuetify,
  store,
  router,
  render: h => h(App),
}).$mount('#app');
