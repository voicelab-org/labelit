<template>
  <div class="test" @click="startTimer"></div>
</template>

<script>

export default {
  name: "MockComponent",
  data(){
    return {
        batch: { project: { timer_inactivity_threshold: 5000 } }, // must be > 1000
    }
  },
};
</script>
