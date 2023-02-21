<template>
  <span>{{ time }}</span>
</template>

<script>
export default {
  name: "TimerDisplay",

  props: {
    seconds: {
      type: Number,
      required: true,
    },
    max: {
      type: Number,
    },
  },
  methods: {
    format(seconds) {
      return (
        String(Math.floor(seconds / 60)) +
        ":" +
        String(Math.floor(seconds % 60)).padStart(2, "0")
      );
    },
  },
  computed: {
    time() {
      return this.format(Math.min(this.seconds, this.computedMax));
    },
    computedMax() {
      return this.max || this.seconds;
    },
  },
};
</script>

<style></style>
