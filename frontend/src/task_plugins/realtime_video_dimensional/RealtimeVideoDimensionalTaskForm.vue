<template>
  <div class="task-form-container">
    <div v-if="step == 0">
      <p style="margin-bottom: 40px">
        Autoplay must be activated in your browser. Please check your browser
        settings if the video does not play or is muted.
      </p>

      <div v-if="!isRealtimeSequenceEnded">
        <MouseTrackingSlider
          v-model="position"
          :do-track="doTrackMousePosition"
        />
        <div v-if="!doTrackMousePosition" class="play-container">
          <v-btn
            rounded
            color="primary"
            @click="
              playVideo();
              doTrackMousePosition = true;
            "
          >
            <v-icon>mdi-play</v-icon>
          </v-btn>
        </div>
      </div>
      <div v-if="isRealtimeSequenceEnded">
        <RealtimeSequenceGraph :sequence="currentRealtimeSequence" />
        <div>
          <v-btn @click="cancelFirstStep()"> Cancel</v-btn>
          <v-btn @click="confirmFirstStep()"> Confirm</v-btn>
        </div>
      </div>
    </div>
    <div v-if="step == 1">
      <p v-if="!secondStepConfirmed">Please assign a global evaluation:</p>
      <v-slider v-model="summativeAnnotation" :thumb-label="'always'" />
      <div>
        <v-btn v-if="!secondStepConfirmed" @click="confirmSecondStep()">
          Confirm
        </v-btn>
      </div>
    </div>
    <div class="guidelines-container">
      <div v-html="task.html_guidelines"></div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue';
import { useVideoPlayer } from '@/composables/video_player.js';
import MouseTrackingSlider from './components/MouseTrackingSlider.vue';
import RealtimeSequenceGraph from './components/RealtimeSequenceGraph.vue';
import TaskForm from '@/components/mixins/TaskForm.js';
import LabelService from '@/services/label.service.js';

const INITIAL_POSITION = 50;
const LABEL_RESOURCE_TYPE = 'RealtimeVideoDimensionalLabel';

export default {
  name: 'RealtimeVideoDimensionalTaskForm',
  components: {
    MouseTrackingSlider,
    RealtimeSequenceGraph,
  },
  mixins: [TaskForm],
  props: {
    videoPlayerLoadedToggle: {
      type: Boolean,
      required: true,
    },
  },
  setup() {
    // composition API
    const { player } = useVideoPlayer();

    return {
      player,
    };
  },
  data() {
    return {
      doTrackMousePosition: false,
      position: INITIAL_POSITION,
      step: 0,
      currentRealtimeSequence: [],
      isRealtimeSequenceEnded: false,
      summativeAnnotation: 50,
      secondStepConfirmed: false,
    };
  },
  watch: {
    currentStepperStep: {
      handler() {
        if (this.currentStepperStep == this.thisFormStepperStep) {
          this.setPlayerOptions();
          this.setupEvents();
        }
      },
    },
    position: {
      handler() {
        this.currentRealtimeSequence.push([
          this.player.currentTime(),
          this.position,
        ]);
      },
    },
    playerLoadedToggle: {
      handler() {
        this.setPlayerOptions();
        this.setupEvents();
      },
    },
  },
  created() {
    this.setPlayerOptions();
    this.setupEvents();
  },
  methods: {
    confirmSecondStep() {
      let label = this.selected_labels[0];
      label.summative = this.summativeAnnotation;
      LabelService.update(label.id, label).then(() => {
        Vue.set(this.selected_labels, 0, label);
        this.secondStepConfirmed = true;
      });
    },
    cancelFirstStep() {
      this.currentRealtimeSequence = [];
      this.isRealtimeSequenceEnded = false;
      this.position = INITIAL_POSITION;
    },
    confirmFirstStep() {
      if (this.selected_labels.length) {
        let label = this.selected_labels[0];
        label.sequence = this.currentRealtimeSequence;
        LabelService.update(label.id, label).then(() => {
          Vue.set(this.selected_labels, 0, label);
        });
      } else {
        LabelService.create({
          resourcetype: LABEL_RESOURCE_TYPE,
          task: this.task.id,
          sequence: this.currentRealtimeSequence,
          summative: INITIAL_POSITION,
        }).then(res => {
          Vue.set(this.selected_labels, 0, res.data);
        });
      }
      this.step++;
    },
    setupEvents() {
      if (this.player) {
        if (this.player.contentEl()) {
          this.player.on('ended', () => {
            this.doTrackMousePosition = false;
            this.isRealtimeSequenceEnded = true;
          });
        }
      }
    },
    playVideo() {
      this.player.currentTime(0);
      this.setupEvents();
      this.player.play();
    },
    setPlayerOptions() {
      this.player.controls(false);
    },
  },
};
</script>

<style lang="scss">
.task-form-container {
  margin-bottom: 15px;

  .play-container {
    display: flex;
    justify-content: center;
  }

  .guidelines-container {
    max-width: 100%;

    img {
      max-width: 100%;
    }
  }
}
</style>
