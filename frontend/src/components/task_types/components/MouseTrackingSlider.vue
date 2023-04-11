<template>
  <div>
    <v-slider v-model="position"></v-slider>
  </div>
</template>

<script>
export default {
  name: 'MouseTrackingSlider',
  data() {
    return {
      position: 0.0,
    };
  },
};
</script>

<style scoped></style>
