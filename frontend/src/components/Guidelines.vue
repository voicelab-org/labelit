<template>
  <div class="guidelines-container">
    <v-menu offset-x>
      <template #activator="{ on, attrs }">
        <v-icon v-bind="attrs" v-on="on"> mdi-information </v-icon>
      </template>
      <div class="guidelines" v-html="task.html_guidelines"></div>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: 'Guidelines',
  props: {
    task: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss">
.guidelines {
  padding: 10px;
  background: white;
  min-height: 200px;
  min-width: 200px;
  max-height: 500px;
  max-width: 500px;
  overflow-y: auto;
}
.guidelines-container {
  display: inline-block;
  margin-left: 5px;
}
</style>
