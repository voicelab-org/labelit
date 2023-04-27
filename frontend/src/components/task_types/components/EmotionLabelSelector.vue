<template>
  <div class="emotion-label-container">
    <div
      v-for="label in labels"
      :class="getLabelClasses(label)"
      @click="$emit('selected', label)"
    >
      {{ label.name }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmotionLabelSelector',
  props: {
    labels: {
      type: Array,
      required: true,
    },
  },
  methods: {
    getLabelClasses(label) {
      return {
        selected: label.intensity !== null,
      };
    },
  },
};
</script>
<style lang="scss">
.emotion-label-container {
  > div {
    border: 1px solid grey;
    padding: 5px 10px;
    cursor: pointer;
    margin-bottom: 5px;
    &.selected {
      background: blue;
      color: white;
    }
    &:hover {
      background: lightblue;
    }
  }
}
</style>
