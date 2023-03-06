<template>
  <v-snackbar v-model="show" :color="color" :timeout="timeout">
    {{ text }}
    <template #action="{ attrs }">
      <v-btn dark text v-bind="attrs" @click="show = false"> Close </v-btn>
    </template>
  </v-snackbar>
</template>
<script>
export default {
  name: 'LabelitSnackbar',
  data() {
    return {
      show: false,
      color: '',
      text: '',
      timeout: -1,
    };
  },
  created() {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === 'snackbar/SHOW_MESSAGE') {
        this.text = state.snackbar.text;
        this.color = state.snackbar.color;
        this.timeout = state.snackbar.timeout;
        this.show = true;
      }
    });
  },
};
</script>
