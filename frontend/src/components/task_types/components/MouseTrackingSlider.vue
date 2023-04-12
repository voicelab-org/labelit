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
      default: 0,
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
  methods: {
    startTracking() {
      // cf. https://codedamn.com/news/javascript/throttling-in-javascript
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
        console.log('event.clientX', event.clientX);
        this.updatePosition(event);
      }, this.throttleDelay);

      window.addEventListener('mousemove', this.throttledMousemoveCallback);
    },
    updatePosition(event) {
      console.log('&updatePosition()');
      let x_position = event.clientX;
      // let container = window.getElementById('');
      console.log(
        'element',
        this.$refs.slidercontainer,
        typeof this.$refs.slidercontainer
      );
      let rect = this.$refs.slidercontainer.getBoundingClientRect();
      console.log(rect.top, rect.right, rect.bottom, rect.left);
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
