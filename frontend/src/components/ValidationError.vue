<template>
  <div v-if="message.length">
    <div class="validation-error">
      {{ message }}
    </div>
  </div>
</template>

<script>
export default {
  name: "ValidationError",
  props: {
    message: {
      type: String,
      default: "",
    },
  },
};
</script>

<style lang="scss">
.validation-error {
  border-radius: 4px;
  margin-top: 15px;
  border: 1px solid red;
}
</style>
