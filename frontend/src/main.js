import Vue from 'vue'
import router from "./router";
import store from "./store/index.js";
import App from './App.vue'

import VJsf from '@koumoul/vjsf'
import '@koumoul/vjsf/dist/main.css'
// load third-party dependencies (markdown-it, vuedraggable)
// you can also load them separately based on your needs
// import '@koumoul/vjsf/dist/third-party.js'

Vue.component('VJsf', VJsf)

import interceptorsSetup from '@/services/interceptors'
interceptorsSetup()

import vuetify from './plugins/vuetify';

import VueShortkey from 'vue-shortkey';
Vue.use(VueShortkey)

//Vue.use(require('vue-shortkey'))

var VueScrollTo = require('vue-scrollto');
Vue.use(VueScrollTo)

/* START auto global component registration */

import upperFirst from 'lodash/upperFirst'
import camelCase from 'lodash/camelCase'

const requireComponent = require.context(
  // The relative path of the components folder
  './components/task_types/',
  // Whether or not to look in subfolders
  false,
  // The regular expression used to match base component filenames
  /[A-Z]\w+\.(vue|js)$/
)


requireComponent.keys().forEach(fileName => {
  // Get component config
  const componentConfig = requireComponent(fileName)

  // Get PascalCase name of component
  const componentName = upperFirst(
    camelCase(
      // Gets the file name regardless of folder depth
      fileName
        .split('/')
        .pop()
        .replace(/\.\w+$/, '')
    )
  )

  // Register component globally
  Vue.component(
    componentName,
    // Look for the component options on `.default`, which will
    // exist if the component was exported with `export default`,
    // otherwise fall back to module's root.
    componentConfig.default || componentConfig
  )
})


/* END auto global component registration */

Vue.config.productionTip = false

new Vue({
      vuetify,
      store,
      router,
      render: h => h(App),
    }).$mount('#app')
