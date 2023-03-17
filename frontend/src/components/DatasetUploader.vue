<template>
  <div>
    <v-btn v-if="!displayForm" @click="displayForm = true" color="primary">
      Import a dataset
    </v-btn>
    <div v-else>
      <file-upload
        ref="upload"
        accept="application/zip"
        :post-action="baseUrl + 'datasets/upload_dataset/'"
        :headers="headers"
        @input-file="inputFile"
        @input-filter="inputFilter"
      >
        <v-btn>{{ fileName || 'Select a file' }}</v-btn>
      </file-upload>
      <v-btn
        :disabled="!fileSelected || importInProgress"
        :loading="importInProgress"
        :style="{ position: 'relative', top: '-17px' }"
        @click.prevent="startUpload()"
      >
        Upload
      </v-btn>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import { baseURL } from '@/app.config.js';
import LocalStorageService from '@/services/local.storage.service.js';
import { SNACKBAR_TYPE_COLOR } from '@/store/snackbar.module.js';

export default {
  name: 'DatasetUploader',
  data() {
    return {
      accessToken: null,
      baseUrl: baseURL,
      displayForm: false,
      importInProgress: false,
      fileName: null,
      fileSelected: false,
      MAX_FILE_NAME: 25,
    };
  },
  computed: {
    headers() {
      return {
        Authorization: `Bearer ${this.accessToken}`,
      };
    },
  },
  created() {
    this.accessToken = LocalStorageService.getAccessToken();
  },
  methods: {
    ...mapActions('snackbar', ['showSnackbar']),
    /**
     * Has changed
     * @param  Object|undefined   newFile   Read only
     * @param  Object|undefined   oldFile   Read only
     * @return undefined
     */
    startUpload: function () {
      this.importInProgress = true;
      this.$refs.upload.active = true;
    },
    inputFile: function (newFile, oldFile) {
      if (newFile && oldFile && !newFile.active && oldFile.active) {
        // Get response data
        if (newFile.xhr) {
          //  Get the response status code
          let notification = {};
          if (newFile.xhr.status === 200) {
            this.dataset_uploaded = true;
            this.$emit('new-dataset-imported');
            notification = {
              text: 'The dataset has been successfully uploaded.',
            };
          } else {
            notification = {
              text: 'Something wrong happened. Contact the support if the problem persist.',
              type: SNACKBAR_TYPE_COLOR.ERROR,
            };
          }
          this.resetForm();
          this.showSnackbar(notification);
        }
      }
    },
    resetForm: function () {
      this.displayForm = false;
      this.fileName = null;
      this.fileSelected = false;
      this.importInProgress = false;
      this.$refs.upload.clear();
    },
    /**
     * Pretreatment
     * @param  Object|undefined   newFile   Read and write
     * @param  Object|undefined   oldFile   Read only
     * @param  Function           prevent   Prevent changing
     * @return undefined
     */
    inputFilter: function (newFile) {
      this.fileSelected = true;
      this.fileName = this.cleanFileName(newFile.name);

      // Create a blob field
      newFile.blob = '';
      let URL = window.URL || window.webkitURL;
      if (URL && URL.createObjectURL) {
        newFile.blob = URL.createObjectURL(newFile.file);
      }
    },
    cleanFileName(dirtyFileName) {
      let fileName = dirtyFileName.trim();
      if (fileName.length > this.MAX_FILE_NAME) {
        fileName = `${fileName.substring(0, this.MAX_FILE_NAME)}...`;
      }
      return fileName;
    },
  },
};
</script>

<style scoped></style>
