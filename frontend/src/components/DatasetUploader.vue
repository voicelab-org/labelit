<template>
  <div>
    <!--<ul>
      <li v-for="file in files" :key="file.name">{{ file.name }} - Error: {{ file.error }}, Success: {{ file.success }}</li>
    </ul>-->
    <div v-if="dataset_uploaded"></div>
    <v-btn v-if="!import_in_progress" @click="import_in_progress = true">
      Import a dataset
    </v-btn>
    <div v-else>
      <div v-if="dataset_uploaded">Import successful.</div>
      <div v-else>
        <file-upload
          ref="upload"
          v-model="files"
          accept="application/zip"
          :post-action="base_url + 'datasets/upload_dataset/'"
          :headers="headers"
          @input-file="inputFile"
          @input-filter="inputFilter"
        >
          <v-btn> 1. Select file </v-btn>
        </file-upload>

        <v-btn
          v-show="!$refs.upload || !$refs.upload.active"
          @click.prevent="$refs.upload.active = true"
          :style="{ position: 'relative', top: '-17px' }"
        >
          2. Upload
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
import { baseURL } from "@/app.config";
import LocalStorageService from "@/services/local.storage.service";

export default {
  name: "DatasetUploader",
  data() {
    return {
      files: [],
      access_token: null,
      base_url: baseURL,
      import_in_progress: false,
      import_complete: false,
      dataset_uploaded: false,
    };
  },
  created() {
    this.access_token = LocalStorageService.getAccessToken();
  },
  computed: {
    headers() {
      return {
        Authorization: `Bearer ${this.access_token}`,
      };
    },
  },
  methods: {
    /**
     * Has changed
     * @param  Object|undefined   newFile   Read only
     * @param  Object|undefined   oldFile   Read only
     * @return undefined
     */
    inputFile: function (newFile, oldFile) {
      console.log("&newFile, oldFile", newFile, oldFile);
      if (newFile && oldFile && !newFile.active && oldFile.active) {
        // Get response data
        console.log("response", newFile.response);
        if (newFile.xhr) {
          //  Get the response status code
          console.log("status", newFile.xhr.status);
          if (200 == newFile.xhr.status) {
            this.dataset_uploaded = true;
            this.$emit("imported");
          }
        }
      }
    },
    /**
     * Pretreatment
     * @param  Object|undefined   newFile   Read and write
     * @param  Object|undefined   oldFile   Read only
     * @param  Function           prevent   Prevent changing
     * @return undefined
     */
    inputFilter: function (newFile) {
      //, oldFile, prevent
      /*if (newFile && !oldFile) {
        // Filter non-image file
        if (!/\.(jpeg|jpe|jpg|gif|png|webp)$/i.test(newFile.name)) {
          return prevent()
        }
      }*/

      // Create a blob field
      newFile.blob = "";
      let URL = window.URL || window.webkitURL;
      if (URL && URL.createObjectURL) {
        newFile.blob = URL.createObjectURL(newFile.file);
      }
    },
  },
  watch: {
    dataset_uploaded() {
      console.log("&change");
    },
  },
};
</script>

<style scoped></style>
