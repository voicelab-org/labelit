<template>
  <div>
    <v-menu
      v-model="open"
      :close-on-content-click="false"
      :nudge-right="0"
      transition="scale-transition"
      origin="left top"
      offset-y
      min-width="290px"
      right
    >
      <template #activator="{ on }">
        <input type="text" :value="displayedDate" readonly v-on="on" />
      </template>

      <v-date-picker
        scrollable
        :value="value"
        :min="minDate"
        :max="maxDate"
        :disabled="is_disabled"
        @input="dateChanged"
      >
      </v-date-picker>
    </v-menu>
  </div>
</template>
<script>
export default {
  name: 'Datepicker',
  props: {
    value: {
      type: String,
    },
    is_disabled: {
      type: Boolean,
    },
    minDate: {
      type: String,
    },
    maxDate: {
      type: String,
    },
  },
  data() {
    return {
      open: false,
    };
  },
  computed: {
    displayedDate: function () {
      return new Date(this.value).toLocaleDateString('en');
    },
  },
  methods: {
    dateChanged(newVal) {
      this.$emit('input', newVal);
      this.$emit('blur');
    },
  },
};
</script>
<style lang="scss">
.v-picker {
  .v-btn,
  button {
    color: grey !important;
    &.v-btn--active {
      .v-btn__content {
        color: white !important;
      }
    }
  }

  .v-date-picker-years {
    li {
      color: grey;
    }
  }
}
</style>
