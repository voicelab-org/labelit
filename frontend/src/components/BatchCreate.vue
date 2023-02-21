<template>
  <div>
    <v-dialog v-model="dialog" persistent max-width="800px">
      <template v-slot:activator="{ on, attrs }">
        <v-btn color="primary" dark v-bind="attrs" v-on="on"> Add Batch </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Create Batch</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-form ref="form" class="mx-2" lazy-validation>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="batchName"
                    label="Batch name"
                    hint="Name of the batch that will be created"
                    :rules="rules.batchNameRules"
                  ></v-text-field>
                </v-col>

                <v-col cols="12">
                  <v-autocomplete
                    v-model="selectedDataset"
                    :items="datasetList"
                    label="Dataset"
                    item-text="name"
                    return-object
                    :rules="rules.datasetRules"
                  ></v-autocomplete>
                  <div v-if="datasetRemainingUnits != null">
                    Remaining units: {{ datasetRemainingUnits }}
                  </div>
                </v-col>
                <v-col cols="12">
                  <v-autocomplete
                    :disabled="!datasetRemainingUnits ? true : false"
                    v-model="selectedAnnotators"
                    :items="annotatorsList"
                    label="Annotators"
                    :item-text="
                      (item) => item.first_name + ' ' + item.last_name
                    "
                    item-value="id"
                    multiple
                    :rules="rules.annotatorsRules"
                  ></v-autocomplete>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model.number="numberOfDocuments"
                    :disabled="!datasetRemainingUnits ? true : false"
                    min="1"
                    :max="datasetRemainingUnits"
                    label="Number of documents"
                    type="number"
                    oninput="if(this.value < 0) this.value = 0;"
                    :rules="rules.numberOfDocumentsRules"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model.number="numberOfAnnotatorsPerDocument"
                    :disabled="!selectedAnnotators.length"
                    min="1"
                    :max="selectedAnnotators.length"
                    label="Number of annotators per document"
                    type="number"
                    oninput="if(this.value < 0) this.value = 0;"
                    :rules="rules.numberOfAnnotatorsPerDocumentRules"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-select
                    :disabled="!datasetRemainingUnits ? true : false"
                    v-model="selectedAnnotationMode"
                    :items="annotationModeList"
                    label="Annotation mode"
                    item-text="description"
                    item-value="value"
                    :rules="rules.annotationModeRules"
                    required
                  ></v-select>
                </v-col>
              </v-row>
            </v-form>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">
            Close
          </v-btn>
          <v-btn color="blue darken-1" text @click="createBatch">
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import ProjectService from "@/services/project.service";
import DatasetService from "@/services/dataset.service";
import BatchService from "@/services/batch.service";
import UserService from "@/services/user.service";

export default {
  name: "BatchCreate",
  props: {
    projectId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      dialog: false,
      datasetList: [],
      selectedDataset: null,
      datasetRemainingUnits: null,
      annotatorsList: [],
      selectedAnnotators: [],
      batchName: null,
      numberOfDocuments: null,
      numberOfAnnotatorsPerDocument: null,
      annotationModeList: [
        {
          value: "all_you_can_annotate",
          description:
            "Annotators can annotate as much they want (up to optional limit) By the end of the batch, annotators may have done unequal amounts of work",
        },
        {
          value: "even",
          description:
            "By the end of the batch, every annotator will have annotated the same number of units",
        },
      ],
      selectedAnnotationMode: null,
      rules: {
        batchNameRules: [
          (v) => !!v || "The Batch Name is required",
          (v) =>
            (v && v.length <= 60) ||
            "The batch name must be less than 60 characters",
        ],
        numberOfDocumentsRules: [
          (v) =>
            !!v ||
            "The number of documents to include to the batch is required and must be a valid number",
          (v) =>
            (v && v >= 1 && v <= this.datasetRemainingUnits) ||
            "The number of documents must not exceed the remaining dataset units",
        ],
        numberOfAnnotatorsPerDocumentRules: [
          (v) =>
            !!v ||
            "The number of annotators per document is required and must be a valid number",
          (v) =>
            (v && v >= 1 && v <= this.datasetRemainingUnits) ||
            "The number of annotators per document must not exceed the number of annotators",
        ],
        annotatorsRules: [(v) => !!v.length || "Select at least one annotator"],
        datasetRules: [(v) => !!v || "Select a dataset"],
        annotationModeRules: [(v) => !!v || "Select an annotation mode"],
      },
    };
  },
  mounted() {
    let vm = this;
    DatasetService.getDatasetList()
      .then(function (response) {
        vm.datasetList = response.data;
      })
      .catch((error) => console.log(error));

    UserService.getUserList()
      .then(function (response) {
        vm.annotatorsList = response.data;
      })
      .catch((error) => console.log(error));
  },
  methods: {
    createBatch() {
      let vm = this;
      if (vm.$refs.form.validate()) {
        BatchService.createBatch({
          name: vm.batchName,
          dataset: vm.selectedDataset.id,
          project: vm.projectId,
          annotators: vm.selectedAnnotators,
          num_documents: vm.numberOfDocuments,
          num_annotators_per_document: vm.numberOfAnnotatorsPerDocument,
          annotation_mode: vm.selectedAnnotationMode,
        })
          .then(function () {
            vm.dialog = false;
            vm.$emit("batchCreated");
          })
          .catch((error) => console.log(error));
      }
    },
  },
  watch: {
    selectedDataset(dataset) {
      let vm = this;
      ProjectService.getRemainingUnitsInDatasetInProject(vm.projectId, {
        dataset_id: dataset.id,
      })
        .then(function (response) {
          vm.datasetRemainingUnits = response.data.count;
        })
        .catch((error) => console.log(error));
    },
  },
};
</script>
