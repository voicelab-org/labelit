import Vue from 'vue';
import upperFirst from 'lodash/upperFirst';
import camelCase from 'lodash/camelCase';

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

export default register_components;
