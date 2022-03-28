<template>
  <div>
    <div v-if="task">
        <h3>{{task.name}}</h3>
        <div>Edit guidelines: </div>
        <vue-editor
            v-model="task.html_guidelines"
            useCustomImageHandler
            @image-added="handleImageAdded"
        ></vue-editor>
    </div>
  </div>
</template>

<script>

import { VueEditor } from "vue2-editor";
import { baseURL } from '@/app.config';

import TaskService from '@/services/task.service.js'
import ImageUploadService from '@/services/image_upload.service.js'

export default {
  name: 'Task',
  components: {
    VueEditor
  },
  props: {
    taskId: {
        type: Number || String,
        required: true,
    },
  },
  data(){
    return {
        task: null,
    }
  },
  created(){
    TaskService.getTaskById(this.taskId)
        .then(
            (res) => {
                this.task = res.data
            }
        )
  },
  watch: {
    'task.html_guidelines': function(){
         TaskService.updateTask(this.task.id, this.task)
     }
  },
  methods: {
   handleImageAdded: function(file, Editor, cursorLocation, resetUploader) {
      // An example of using FormData
      // NOTE: Your key could be different such as:
      // formData.append('file', file)

      var formData = new FormData();
      formData.append("image", file);
      ImageUploadService.upload(formData)
        .then(res => {
          let url = res.data.url; // Get url from response
          Editor.insertEmbed(cursorLocation, "image", baseURL.substring(0, baseURL.length - 1) + url);
          resetUploader();
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
}
</script>

<style lang="scss" scoped></style>


