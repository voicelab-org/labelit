<template>
  <div id="blue-filter-overlay" :style="overlayStyle">
    <slot></slot>
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

export default {
  name: 'BlueFilter',
  computed: {
    ...mapGetters({
      percentage: 'blueFilter/percentage',
    }),
    overlayStyle() {
      return {
        background: 'rgba(255, 255, 0, ' + this.percentage / 100 + ')',
      };
    },
  },
};
</script>

<style lang="scss">
#blue-filter-overlay {
  position: fixed;
  background-blend-mode: multiply;
  pointer-events: none;
  opacity: 0.5;
  min-height: 100vh;
  width: 100%;
  z-index: 200000;
  top: 0;
  left: 0;
  height: 100vh;
}
</style>
