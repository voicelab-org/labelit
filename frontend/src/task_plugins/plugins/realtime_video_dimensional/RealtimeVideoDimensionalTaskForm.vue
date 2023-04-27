<template>
  <div class="task-form-container">
    <div v-if="step == 0">
      <p>
        Autoplay must be activated in your browser. Please check your browser
        settings if the video does not play or is muted.
      </p>

      <p />
      <div v-if="!is_realtime_sequence_ended">
        <MouseTrackingSlider
          :do-track="do_track_mouse_position"
          v-model="position"
        />
        <div class="play-container" v-if="!do_track_mouse_position">
          <v-btn
            rounded
            color="primary"
            @click="
              playVideo();
              do_track_mouse_position = true;
            "
          >
            <v-icon>mdi-play</v-icon>
          </v-btn>
        </div>
      </div>
      <div v-if="this.is_realtime_sequence_ended">
        <RealtimeSequenceGraph :sequence="current_realtime_sequence" />
        <div>
          <v-btn @click="cancelFirstStep()"> Cancel</v-btn>
          <v-btn @click="confirmFirstStep()"> Confirm</v-btn>
        </div>
      </div>
    </div>
    <div v-if="step == 1">
      <p v-if="!second_step_confirmed">Please assign a global evaluation:</p>
      <v-slider :thumb-label="true" v-model="summative_annotation" />
      <div>
        <v-btn @click="confirmSecondStep()" v-if="!second_step_confirmed">
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
import MouseTrackingSlider from '@/components/task_types/components/MouseTrackingSlider.vue';
import RealtimeSequenceGraph from '@/components/task_types/components/RealtimeSequenceGraph.vue';
import TaskForm from '@/components/mixins/TaskForm.js';
import LabelService from '@/services/label.service.js';

const INITIAL_POSITION = 50;
const LABEL_RESOURCE_TYPE = 'RealtimeVideoDimensionalLabel';

export default {
  name: 'RealtimeVideoDimensionalTaskForm',
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
      do_track_mouse_position: false,
      position: INITIAL_POSITION,
      step: 0,
      current_realtime_sequence: [],
      is_realtime_sequence_ended: false,
      summative_annotation: 50,
      second_step_confirmed: false,
    };
  },
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
  created() {
    this.setPlayerOptions();
    this.setupEvents();
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
        this.current_realtime_sequence.push([
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
  methods: {
    confirmSecondStep() {
      let label = this.selected_labels[0];
      label.summative = this.summative_annotation;
      LabelService.update(label.id, label).then(() => {
        Vue.set(this.selected_labels, 0, label);
        this.second_step_confirmed = true;
      });
    },
    cancelFirstStep() {
      this.current_realtime_sequence = [];
      this.is_realtime_sequence_ended = false;
      this.position = INITIAL_POSITION;
    },
    confirmFirstStep() {
      if (this.selected_labels.length) {
        let label = this.selected_labels[0];
        label.sequence = this.current_realtime_sequence;
        LabelService.update(label.id, label).then(() => {
          Vue.set(this.selected_labels, 0, label);
        });
      } else {
        LabelService.create({
          resourcetype: LABEL_RESOURCE_TYPE,
          task: this.task.id,
          sequence: this.current_realtime_sequence,
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
            this.do_track_mouse_position = false;
            this.is_realtime_sequence_ended = true;
          });
        }
      }
    },
    playVideo() {
      setTimeout(
        () => {
          this.player.currentTime(0);
          this.setupEvents();
          this.player.play();
        },
        10 // HACK
      );
    },
    setPlayerOptions() {
      let current_options = this.player.options();

      if (current_options.controls) {
        this.playerOptions = this.player.options({
          controls: false,
        });
      }
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
