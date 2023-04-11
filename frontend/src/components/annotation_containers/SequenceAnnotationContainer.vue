<template>
  <div>
    <span
      v-shortkey="['ctrl', 'alt', 'arrowright']"
      @shortkey.stop="next()"
    ></span>
    <span
      v-shortkey="['ctrl', 'alt', 'arrowleft']"
      @shortkey.stop="previous()"
    ></span>
    <v-card elevation="0">
      <div class="bv-section">
        <v-stepper v-model="step" elevation="0">
          <v-stepper-header>
            <v-stepper-step
              v-for="(annotation, i) in annotations"
              :key="annotation.id"
              :complete="step > i + 1"
              :step="i + 1"
            >
              {{ getTaskName(i) }}
            </v-stepper-step>
          </v-stepper-header>

          <v-stepper-items>
            <v-stepper-content
              v-for="(annotation, i) in annotations"
              :key="annotation.id"
              :step="i + 1"
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

              <div>
                <v-btn v-if="i != 0" @click="previous(i)"> Previous </v-btn>
                <v-btn
                  color="primary"
                  @click="next(i)"
                  v-if="i < annotations.length - 1"
                >
                  Next
                </v-btn>
              </div>
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </div>
    </v-card>
  </div>
</template>

<script>
import AnnotationContainer from './mixins/AnnotationContainer';

export default {
  name: 'SequenceAnnotationContainer',
  mixins: [AnnotationContainer],
  props: {
    annotations: {
      type: Array,
      required: true,
    },
    tasks: {
      type: Array,
      required: true,
    },
    time: {
      type: Number,
    },
    submitting: {
      type: Boolean,
      required: true,
    },
    reviewMode: {
      type: Boolean,
    },
  },
  data() {
    return {
      focus_index: 0,
      step: 1,
    };
  },
  methods: {
    getTaskName(annotation_index) {
      return this.tasks.find(
        t => t.id == this.annotations[annotation_index].task
      ).name;
    },
    next() {
      this.step = this.step + 1;
    },
    previous() {
      if (this.step == 1) return;
      this.step = this.step - 1;
    },
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
