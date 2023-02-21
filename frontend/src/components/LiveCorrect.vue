<template>
  <div>
    <div class="live-correct-container" id="live-correct-container">
      <div
        v-for="(segment, idx) in sortedSegments"
        :key="segment.id"
        :class="getSegmentClasses(segment)"
        :ref="segment.id"
      >
        <form v-on:submit.prevent="blurInput($event, 'input-' + segment.id)">
          <textarea
            rows="1"
            type="text"
            v-model="sortedSegments[idx].transcript"
            @input="textareaInputEvent($event, idx)"
            @focus="is_focused = true"
            @blur="is_focused = false"
            :ref="'input-' + segment.id"
            :disabled="readOnly"
          />
        </form>
      </div>
    </div>
  </div>
</template>

<script>
var VueScrollTo = require("vue-scrollto");

export default {
  name: "live-correct",
  props: {
    readOnly: {
      type: Boolean,
      default: false,
    },
    playbackTime: {
      type: Number,
      required: true,
    },
    value: {
      type: Object,
      default() {
        return {
          id: 12,
          segments: [
            {
              transcript: "Oui bonjour je souhaite annuler ma réservation",
              id: 0,
              start_time: 0.0,
            },
            {
              transcript: "à cause d'un imprévu",
              id: 1,
              start_time: 3.0,
            },
            {
              transcript: "je pense revenir cet été cependant",
              id: 2,
              start_time: 5.0,
            },
            {
              transcript: "ça dépend de comment la situation évolue",
              id: 3,
              start_time: 7.0,
            },
          ],
        };
      },
    },
  },
  computed: {
    sortedSegments() {
      return [...this.timed_transcript.segments].sort((a, b) => {
        return a.start_time - b.start_time;
      });
    },
  },
  data() {
    return {
      timed_transcript: this.value,
      cursor_segment_id: null,
      is_focused: false,
    };
  },
  mounted() {
    this.timed_transcript.segments.forEach((seg) => {
      this.fitTextareaToText(this.$refs["input-" + seg.id][0]);
    });
  },
  watch: {
    timed_transcript: {
      deep: true,
      handler() {
        this.$emit("input", this.timed_transcript);
      },
    },
    playbackTime() {
      this.cursor_segment_id = this.segmentBinarySearch(
        this.sortedSegments,
        this.playbackTime
      );
      this.scrollTo(this.cursor_segment_id);
    },
  },
  methods: {
    textareaInputEvent($event, idx) {
      this.sortedSegments[idx].touched = true;
      this.$nextTick(() => {
        this.fitTextareaToText($event.target);
      });
    },
    fitTextareaToText(el) {
      el.style.height = "";
      el.style.height = el.scrollHeight + "px";
    },
    blurInput($event, ref) {
      this.$refs[ref][0].blur();
    },
    scrollTo(id) {
      if (this.is_focused) return;
      var options = {
        container: "#live-correct-container",
        lazy: false,
        offset: -60,
        force: true,
        cancelable: true,
        x: false,
        y: true,
      };

      var element = this.$refs[id][0];
      var duration = 0;

      VueScrollTo.scrollTo(element, duration, options);
    },
    segmentBinarySearch(arr, val) {
      if (val == 0) {
        return arr[0];
      }
      if (val > arr[arr.length - 1].start_time) {
        return arr[arr.length - 1].id;
      }
      let startIdx = 0;
      let endIdx = arr.length - 1;
      while (endIdx > startIdx) {
        var midIdx = Math.floor((startIdx + endIdx) / 2);
        if (arr[midIdx].start_time > val) {
          endIdx = midIdx;
        } else if (arr[midIdx].start_time < val) {
          startIdx = midIdx + 1;
        } else {
          return arr[midIdx].id;
        }
      }
      return arr[startIdx - 1].id;
    },
    getSegmentClasses(segment) {
      return {
        segment: true,
        "cursor-active": segment.id == this.cursor_segment_id,
      };
    },
  },
};
</script>

<style lang="scss">
.live-correct-container {
  border: 1px solid lightgrey;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
  .segment {
    padding-left: 10px;
    &.cursor-active {
      border-left: 2px solid #03a9f4;
    }
    textarea {
      padding-top: 8px;
      width: 100%;
    }
  }
}
</style>
