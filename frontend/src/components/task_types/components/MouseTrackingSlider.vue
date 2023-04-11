<template>
  <div>
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

      window.addEventListener(
        'mousemove',
        throttle(event => {
          console.log('event.clientX', event.clientX);
        }, this.throttleDelay)
      );
    },
    recordPosition() {},
  },
  watch: {
    doTrack: {
      handler() {
        if (this.doTrack) {
          this.startTracking();
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

<style scoped></style>
