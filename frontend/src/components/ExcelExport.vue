<template>
  <v-icon color="primary" :title="'Export data'" @click="exportExcel">
    mdi-download-box
  </v-icon>
</template>

<script>
import { json2excel } from 'js2excel';

export default {
  name: 'ExcelExport',
  props: {
    data: {
      type: Array,
    },
    name: {
      type: String,
    },
  },
  methods: {
    exportExcel() {
      let data = this.data;
      let name = this.name;

      // this will be export a excel and the file's name is user-info-data.xlsx
      // the default file's name is excel.xlsx
      try {
        json2excel({
          data,
          name: 'export-' + name,
          formateDate: 'yyyy-mm-dd',
        });
      } catch (error) {
        console.error('error');
      }
    },
  },
};
</script>

<style scoped></style>
