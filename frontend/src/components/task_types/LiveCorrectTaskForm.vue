<template>
  <div class="live-correct-task-form-container">
    <TaskFormHeader :task="task" :read-only="readOnly" />
    <LiveCorrect
      v-if="timed_transcript"
      :playback-time="playbackTime"
      v-model="timed_transcript"
      :read-only="readOnly"
    />
  </div>
</template>
<script>
import Vue from "vue";
import TaskForm from "@/components/mixins/TaskForm";
import TaskFormHeader from "@/components/TaskFormHeader";
import LiveCorrect from "@/components/LiveCorrect";
import LabelService from "@/services/label.service.js";
import TimedTranscriptService from "@/services/timed_transcript.service.js";
import { mapGetters } from "vuex";

export default {
  name: "live-correct-task-form",
  mixins: [TaskForm],
  components: {
    TaskFormHeader,
    LiveCorrect,
  },
  computed: {
    ...mapGetters({
      playbackTime: "player/playbackTime",
    }),
  },
  data() {
    return {
      timeout: null,
      timed_transcript: null,
      label: null,
    };
  },
  created() {
    if (!this.selected_labels.length) {
      let transcript = JSON.parse(
        JSON.stringify(this.document.timed_transcript)
      );
      delete transcript.id;
      transcript.segments.forEach((s) => {
        delete s.id;
        //delete s.timed_transcript
      });
      TimedTranscriptService.create(transcript).then((res) => {
        var created_transcript = res.data;
        LabelService.create({
          resourcetype: "LiveCorrectLabel",
          timed_transcript: created_transcript.id,
          task: this.task.id,
        }).then((res) => {
          this.timed_transcript = created_transcript;
          this.label = res.data;
        });
      });
    } else {
      LabelService.get(this.selected_labels[0].id).then((res) => {
        this.label = res.data;
        this.timed_transcript = this.label.timed_transcript;
      });
    }
  },
  watch: {
    timed_transcript: {
      deep: true,
      handler() {
        clearTimeout(this.timeout);
        // this is where live correct labels get created/updated
        this.timeout = setTimeout(() => {
          TimedTranscriptService.update(
            this.timed_transcript.id,
            this.timed_transcript
          ).then(() => {
            LabelService.update(this.label.id, this.label).then(() => {
              Vue.set(this.selected_labels, 0, this.label);
            });
          });
        }, 1000);
      },
    },
  },
};
</script>

<style lang="scss"></style>
