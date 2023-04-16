<template>
  <div class="emotion-task-form-container">
    <div v-if="negative_labels && positive_labels">
      <EmotionLabelSelector
        :labels="negative_labels"
        @selected="initializeLabelIntensitySetting"
      />
      <div>
        <div v-if="show_intensity_slider">
          <v-slider v-model="intensity_position"></v-slider>
          <v-btn v-if="!intensity_confirmed" @click="confirmIntensity">
            CONFIRM
          </v-btn>
        </div>
      </div>
      <EmotionLabelSelector
        :labels="positive_labels"
        @selected="initializeLabelIntensitySetting"
      />
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import { useVideoPlayer } from '@/composables/video_player.js';
import TaskForm from '@/components/mixins/TaskForm.js';
import LabelService from '@/services/label.service.js';

import EmotionLabelSelector from '@/components/task_types/components/EmotionLabelSelector.vue';

const LABEL_RESOURCE_TYPE = 'EmotionCategoricalLabel';

const NEGATIVE_LABELS = ['Coupable', 'Ennuyé', 'Vexé'];
const POSITIVE_LABELS = ["Plein d'espoir", 'Fier', 'Excité'];
const INITIAL_POSITION = 50;

export default {
  name: 'EmotionCategoricalTaskForm',
  setup() {
    // composition API
    const { player, playerOptions } = useVideoPlayer();

    return {
      player,
      playerOptions,
    };
  },
  data() {
    return {
      negative_labels: this.initializeLabels(NEGATIVE_LABELS),
      positive_labels: this.initializeLabels(POSITIVE_LABELS),
      intensity_position: INITIAL_POSITION,
      show_intensity_slider: false,
      intensity_confirmed: false,
      current_label: null,
    };
  },
  mounted() {
    console.log('&mounted');
  },
  components: {
    EmotionLabelSelector,
  },
  mixins: [TaskForm],
  props: {
    videoPlayerLoadedToggle: {
      type: Boolean,
      required: true,
    },

    //HACK

    currentStepperStep: {
      type: Number,
    },
    thisFormStepperStep: {
      type: Number,
    },
    // END HACK
  },
  created() {
    this.setPlayerOptions();
  },
  watch: {
    playerLoadedToggle: {
      handler() {
        this.setPlayerOptions();
      },
    },
    currentStepperStep: {
      handler() {
        if (this.currentStepperStep == this.thisFormStepperStep) {
          this.setPlayerOptions();
        }
      },
    },
  },
  methods: {
    confirmIntensity() {
      this.current_label.intensity = this.intensity_position;

      this.intensity_confirmed = true;
      // TODO create or update label, then set this.selected_labels[0]
      // Vue.set(this.selected_labels, 0, this.positive_labels.concat(this.negative_labels));
    },
    initializeLabels(label_names) {
      let labels = [];

      label_names.forEach(n => {
        labels.push({
          name: n,
          intensity: null,
        });
      });
      return labels;
    },
    initializeLabelIntensitySetting(label) {
      this.intensity_confirmed = false;
      this.show_intensity_slider = true;
      if (label.intensity) {
        this.intensity_position = label.intensity;
      } else {
        this.intensity_position = INITIAL_POSITION;
      }
      this.current_label = label;
    },
    setPlayerOptions() {
      let current_options = this.player.options();

      if (!current_options.controls) {
        this.playerOptions = this.player.options({
          controls: true,
        });
      }
    },
  },
};
</script>

<style lang="scss">
.emotion-task-form-container {
  > div {
    display: flex;
    justify-content: space-between;
    > div:nth-child(2) {
      min-width: 300px;
      .v-btn {
        margin: 0 auto !important;
        display: block !important;
      }
    }
  }

  margin-bottom: 15px;
}
</style>
