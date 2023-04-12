<template>
  <div :id="sliderContainerId" ref="slidercontainer">
    <v-slider v-model="position"></v-slider>
  </div>
</template>

<script>
export default {
  name: 'MouseTrackingSlider',
  props: {
    doTrack: {
      type: Boolean,
      default: false,
    },
    value: {
      type: Number,
      default: 50,
    },
    throttleDelay: {
      type: Number,
      default: 10, //10 ms
    },
  },
  data() {
    return {
      position: this.value,
      sliderContainerId: 'slider-container',
      throttledMousemoveCallback: null,
    };
  },
  computed: {
    sliderContainerDOMRectangle() {
      return this.$refs.slidercontainer.getBoundingClientRect();
    },
  },
  methods: {
    startTracking() {
      // TODO consider using lodash throttle function: `_.throttle()`
      function throttle(cb, delay) {
        let wait = false;
        let storedArgs = null;

        function checkStoredArgs() {
          if (storedArgs == null) {
            wait = false;
          } else {
            cb(...storedArgs);
            storedArgs = null;
            setTimeout(checkStoredArgs, delay);
          }
        }

        return (...args) => {
          if (wait) {
            storedArgs = args;
            return;
          }

          cb(...args);
          wait = true;
          setTimeout(checkStoredArgs, delay);
        };
      }

      this.throttledMousemoveCallback = throttle(event => {
        this.updatePosition(event);
      }, this.throttleDelay);

      window.addEventListener('mousemove', this.throttledMousemoveCallback);
    },
    updatePosition(event) {
      let rect = this.sliderContainerDOMRectangle;
      let rect_width = rect.right - rect.left;
      let x_position = Math.min(
        Math.max(0, event.clientX - rect.left),
        rect_width
      );
      this.position = Math.round((100 * x_position) / rect_width);
    },
    stopTracking() {
      window.removeEventListener('mousemove', this.throttledMousemoveCallback);
    },
  },
  watch: {
    doTrack: {
      handler() {
        if (this.doTrack) {
          this.startTracking();
        } else {
          this.stopTracking();
        }
      },
    },
    position: {
      handler() {
        this.$emit('input', this.position);
      },
    },
  },
};
</script>

<style lang="scss">
#slider-container {
  .v-slider--horizontal {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
}
</style>
