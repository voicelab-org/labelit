<template>
  <div class="emotion-task-form-container">
    <div v-if="negative_labels && positive_labels && user">
      <EmotionLabelSelector
        :labels="sorted_negative_labels"
        @selected="initializeLabelIntensitySetting"
      />
      <div>
        <div v-if="show_intensity_slider" style="margin-top: 50px">
          <template v-if="!intensity_confirmed">
            <v-slider
              v-model="intensity_position"
              :thumb-label="'always'"
            ></v-slider>
            <v-btn @click="confirmIntensity"> CONFIRM </v-btn>
          </template>
        </div>
      </div>
      <EmotionLabelSelector
        :labels="sorted_positive_labels"
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

import EmotionLabelSelector from './components/EmotionLabelSelector.vue';
import { mapGetters } from 'vuex';

const LABEL_RESOURCE_TYPE = 'EmotionCategoricalLabel';

const NEGATIVE_LABELS = ['Coupable', 'Vexé', 'Ennuyé'];
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
      annotation_label: null,
    };
  },
  computed: {
    ...mapGetters({
      user: 'auth/user',
    }),
    sorted_negative_labels() {
      return this.sortLabels(this.negative_labels);
    },
    sorted_positive_labels() {
      return this.sortLabels(this.positive_labels);
    },
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
    user: {
      deep: true,
      handler() {
        console.log('user chged', JSON.parse(JSON.stringify(this.user)));
      },
    },
  },
  methods: {
    sortLabels(labels) {
      if (!this.user) return [];
      //cf. https://itecnote.com/tecnote/javascript-seeding-the-random-number-generator-in-javascript/
      function sfc32(a, b, c, d) {
        return function () {
          a |= 0;
          b |= 0;
          c |= 0;
          d |= 0;
          var t = (((a + b) | 0) + d) | 0;
          d = (d + 1) | 0;
          a = b ^ (b >>> 9);
          b = (c + (c << 3)) | 0;
          c = (c << 21) | (c >>> 11);
          c = (c + t) | 0;
          return (t >>> 0) / 4294967296;
        };
      }

      function xmur3(str) {
        for (var i = 0, h = 1779033703 ^ str.length; i < str.length; i++)
          (h = Math.imul(h ^ str.charCodeAt(i), 3432918353)),
            (h = (h << 13) | (h >>> 19));
        return function () {
          h = Math.imul(h ^ (h >>> 16), 2246822507);
          h = Math.imul(h ^ (h >>> 13), 3266489909);
          return (h ^= h >>> 16) >>> 0;
        };
      }

      // Create xmur3 state:
      var seed = xmur3(this.user.email);
      // Output four 32-bit hashes to provide the seed for sfc32.
      var rand = sfc32(seed(), seed(), seed(), seed());

      function _shuffle(array) {
        var m = array.length,
          t,
          i;

        // While there remain elements to shuffle…
        while (m) {
          // Pick a remaining element…
          /*
          let random_number_1 = Math.random(seed)
          console.log("&random_number_1", random_number_1)
          */
          //i = Math.floor(random_number_1 * m--);
          let rand_value = rand();
          if (rand_value > 0.5) {
            var random_number = 1 - rand_value;
          } else {
            random_number = rand_value;
          }
          i = Math.floor(random_number * m--);
          // And swap it with the current element.
          t = array[m];
          array[m] = array[i];
          array[i] = t;
          ++seed;
        }

        return array;
      }
      return _shuffle(labels);
    },
    confirmIntensity() {
      this.current_label.intensity = this.intensity_position;

      this.intensity_confirmed = true;
      if (!this.annotation_label) {
        LabelService.create({
          resourcetype: LABEL_RESOURCE_TYPE,
          task: this.task.id,
          tags_with_intensities: this.sorted_positive_labels.concat(
            this.sorted_negative_labels
          ),
        }).then(res => {
          this.annotation_label = res.data;
          Vue.set(this.selected_labels, 0, res.data);
        });
      } else {
        let payload = {
          resourcetype: LABEL_RESOURCE_TYPE,
          tags_with_intensities: this.sorted_positive_labels.concat(
            this.sorted_negative_labels
          ),
        };
        LabelService.update(this.annotation_label.id, payload).then(() => {
          Vue.set(this.selected_labels, 0, {
            ...payload,
            id: this.annotation_label.id,
          });
        });
      }
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

      //TODO randomize order based on username

      return labels;
    },
    initializeLabelIntensitySetting(label) {
      console.log('&this.user', this.user);
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
