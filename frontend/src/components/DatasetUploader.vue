<template>
  <div>
    <ul>
      <li v-for="file in files" :key="file.name">{{ file.name }} - Error: {{ file.error }}, Success: {{ file.success }}</li>
    </ul>
    <file-upload
        ref="upload"
        v-model="files"
        accept="application/zip"
        :post-action="base_url + 'datasets/upload_dataset/'"
        :headers="headers"
        @input-file="inputFile"
        @input-filter="inputFilter"
    ><!-- TODO: un-hardcode URLs; issue with forwarding to url froù :8081 to :8080 if url root not specified-->
      <!--ost-action="http://127.0.0.1:8000/api/datasets/upload_dataset/"-->
      <v-btn>
        Select file
      </v-btn>
    </file-upload>

    <v-btn
        color="primary"
        v-show="!$refs.upload || !$refs.upload.active" @click.prevent="$refs.upload.active = true"
        :style="{position: 'relative', top: '-17px'}"
    >
      Start Upload
    </v-btn>
    <button v-show="$refs.upload && $refs.upload.active" @click.prevent="$refs.upload.active = false" type="button">Stop
      <v-btn>
        Upload
      </v-btn>
    </button>
  </div>
</template>

<script>

import { baseURL } from '@/app.config';



import LocalStorageService from '@/services/local.storage.service'


export default {
  name: "DatasetUploader",
  data() {
    return {
      files: [],
      access_token: null,
      base_url: baseURL,
    }
  },
  created(){

    this.access_token = LocalStorageService.getAccessToken()
  },
  computed:{
    headers(){
      return {
        "Authorization": `Bearer ${this.access_token}`,
      }
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
      console.log("&newFile, oldFile", newFile, oldFile)
      if (newFile && oldFile && !newFile.active && oldFile.active) {
        // Get response data
        console.log('response', newFile.response)
        if (newFile.xhr) {
          //  Get the response status code
          console.log('status', newFile.xhr.status)
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
    inputFilter: function (newFile) {//, oldFile, prevent
      /*if (newFile && !oldFile) {
        // Filter non-image file
        if (!/\.(jpeg|jpe|jpg|gif|png|webp)$/i.test(newFile.name)) {
          return prevent()
        }
      }*/

      // Create a blob field
      newFile.blob = ''
      let URL = window.URL || window.webkitURL
      if (URL && URL.createObjectURL) {
        newFile.blob = URL.createObjectURL(newFile.file)
      }
    }
  },
}
</script>

<style scoped>

</style>