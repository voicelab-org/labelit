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

// BEGIN add vue-video-player@5.0.2
import VueVideoPlayer from 'vue-video-player';

// require videojs style
import 'video.js/dist/video-js.css';
// import 'vue-video-player/src/custom-theme.css'

Vue.use(
  VueVideoPlayer /* {
  options: global default options,
  events: global videojs events
} */
);
// END add vue-video-player@5.0.2

// We must register these components because they will be dynamically called

function register_components(files) {
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
}

// BEGIN Annotation container types registration
const container_files = import.meta.globEager(
  '@/components/annotation_containers/*.vue'
);
register_components(container_files);
// END

// BEGIN Task types registration
const files = import.meta.globEager('@/components/task_types/*.vue');
register_components(files);
// END Task types registration

Vue.config.productionTip = false;

new Vue({
  i18n,
  vuetify,
  store,
  router,
  render: h => h(App),
}).$mount('#app');
