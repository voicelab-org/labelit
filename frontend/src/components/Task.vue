<template>
  <div>
    <div class="d-flex align-center">
      <v-btn icon @click="$router.push('/tasks')">
        <v-icon> mdi-arrow-left </v-icon>
      </v-btn>
      <h2 class="headline">Task: {{ task?.name }}</h2>
    </div>
    <div class="mt-12">Edit guidelines:</div>
    <vue-editor
      v-if="task"
      v-model="task.html_guidelines"
      class="mt-5"
      use-custom-image-handler
      @image-added="handleImageAdded"
    ></vue-editor>
  </div>
</template>

<script>
import { VueEditor } from 'vue2-editor';
import { baseURL } from '@/app.config';

import TaskService from '@/services/task.service.js';
import ImageUploadService from '@/services/image_upload.service.js';

export default {
  name: 'Task',
  components: {
    VueEditor,
  },
  props: {
    taskId: {
      type: Number || String,
      required: true,
    },
  },
  data() {
    return {
      task: null,
      loading: true,
    };
  },
  watch: {
    'task.html_guidelines': function () {
      if (this.loading) return;
      TaskService.updateTask(this.task.id, this.task);
    },
  },
  created() {
    TaskService.getTaskById(this.taskId)
      .then(res => {
        this.task = res.data;
      })
      .finally(() => {
        this.loading = false;
      });
  },
  methods: {
    handleImageAdded: function (file, Editor, cursorLocation, resetUploader) {
      // An example of using FormData
      // NOTE: Your key could be different such as:
      // formData.append('file', file)

      var formData = new FormData();
      formData.append('image', file);
      ImageUploadService.upload(formData)
        .then(res => {
          let url = res.data.url; // Get url from response
          Editor.insertEmbed(
            cursorLocation,
            'image',
            baseURL.substring(0, baseURL.length - 1) + url
          );
          resetUploader();
        })
        .catch(err => {
          console.error(err);
        });
    },
  },
};
</script>
