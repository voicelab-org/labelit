<template>
  <div>
    <span
      v-shortkey="['ctrl', 'alt', 'arrowup']"
      @shortkey.stop="browseTasks('left')"
    ></span>
    <span
      v-shortkey="['ctrl', 'alt', 'arrowdown']"
      @shortkey.stop="browseTasks('right')"
    ></span>
    <span
      v-shortkey="['ctrl', 'alt', 'arrowup']"
      @shortkey.stop="browseTasks('left')"
    ></span>
    <span
      v-shortkey="['ctrl', 'alt', 'arrowdown']"
      @shortkey.stop="browseTasks('right')"
    ></span>
    <div v-if="sorted_annotations" id="annotation-forms-t">
      <div
        v-for="(annotation, i) in sorted_annotations"
        :key="annotation.id"
        :class="getAnnotationClasses(annotation, i == focus_index)"
      >
        <component
          :is="getFormForTask(getTaskForAnnotation(annotation))"
          :annotation="annotation"
          :time="time"
          :task="getTaskForAnnotation(annotation)"
          :submitting="submitting"
          :review-mode="reviewMode"
          :document="document"
          :focused="i == focus_index"
          @submitted="$emit('submitted')"
          @submiterror="$emit('submiterror')"
          @focus="focus_index = i"
        />
        <div v-if="annotation.qa_invalidation_comment">
          {{ annotation.qa_invalidation_comment }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AnnotationContainer from './mixins/AnnotationContainer';

export default {
  name: 'ListAnnotationContainer',
  mixins: [AnnotationContainer],
  props: {},
  data() {
    return {
      focus_index: 0,
    };
  },
  methods: {
    browseTasks(direction) {
      if (direction == 'right') {
        if (this.focus_index == this.annotations.length - 1) {
          this.focus_index = 0;
        } else {
          this.focus_index++;
        }
      }

      if (direction == 'left') {
        if (this.focus_index == 0) {
          this.focus_index = this.annotations.length - 1;
        } else {
          this.focus_index--;
        }
      }
    },
  },
};
</script>

<style scoped></style>
