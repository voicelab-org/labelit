<template>
  <div class="task-form-container">
    <TaskFormHeader
        :task="task"
        :read-only="readOnly"
    />
    <br>
    <div id="region-info" v-if="!readOnly">
      Highlight regions in the audio player displayed above. Double-click on a region to remove it.
    </div>
    <span v-show="false"> Selected labels: {{ selected_labels }} </span>
    <!--HACK,  TODO: understand why it breaks after removing this line-->

    <div v-if="readOnly">
      <v-checkbox v-model="showAnnotatedRegions">
        <div slot="label">
          Show annotations
        </div>
      </v-checkbox>
    </div>

    <div class="current-labels">
      <div
          v-for="(val, key) in ordered_selected_labels"
          :key="key"
          style="margin-bottom:5px;"
      >
        <v-chip
            pill
            small
            text-color="darkgrey"
        >
          {{ val.start.toFixed(2) }} -> {{ val.end.toFixed(2) }}
        </v-chip>
      </div>
    </div>
  </div>
</template>
<script>


import TaskForm from '@/components/mixins/TaskForm'
import TaskFormHeader from '@/components/TaskFormHeader'
import {mapGetters} from 'vuex'
import AnnotationService from "@/services/annotation.service";
import LabelService from "@/services/label.service";

export default {
  name: 'region-task-form',
  components: {
    TaskFormHeader,
  },
  mixins: [TaskForm],
  computed: {
    ...mapGetters({
      region_tasks: 'regions/region_tasks',
      annotated_regions: 'regions/annotated_regions',
    }),
    ordered_selected_labels() {
      let ordered = [...this.selected_labels]
      ordered.sort((a, b) => {
        return a.start > b.start
      })
      return ordered
    },
    /*grouped_selected_labels() {

      if (!this.annotated_regions.length) {
        return {}
      }
      let grouped = this.groupBy(this.selected_labels, 'name')
      return grouped
    },*/
  },
  created() {
    this.$store.commit('regions/ADD_TASK', this.task)

    // initial setup of initial state in DB
    let selected_labels = []
    let promises = []


    this.annotation.labels.forEach(
        (id) => {
          promises.push(
              LabelService.get(id).then(res => selected_labels.push(res.data))
          )
        }
    )
    Promise.all(promises).then(
        () => {
          this.selected_labels = selected_labels
          if (!this.readOnly) {
            this.$store.commit('regions/ADD_ANNOTATED_REGIONS', this.selected_labels)
          }
        }
    )
  },
  data() {
    return {
      labels_to_add: [],
      showAnnotatedRegions: false,
      isMixinWatcherActive: false,
    }
  },
  watch: {
    showAnnotatedRegions() {
      if (this.showAnnotatedRegions) {
        this.$store.commit('regions/SET_ANNOTATED_REGIONS', this.selected_labels)
      } else {
        this.$store.commit('regions/SET_ANNOTATED_REGIONS', [])
      }
    },
    annotated_regions() {
      console.log("&annotated_regions changed")
      if (this.readOnly) return
      this.selected_labels = this.annotated_regions.filter(
          (e) => {
            return e.task == this.task.id
          }
      )
      console.log('&seld labls', this.selected_labels)
    },
    selected_labels: {
      deep: true,
      handler(newLabels, oldLabels) {
        console.log("&labels changed", JSON.stringify(newLabels), oldLabels)
        let vm = this
        var editedAnnotation = {}
        Object.assign(editedAnnotation, vm.annotation)
        let promises = []
        /*this.selected_labels.forEach(
            (selected_label) => {
              let is_label_in_labels_to_add = this.labels_to_add.find(
                  (l) => {
                    return l.start == selected_label.start && l.end == selected_label.end
                  }
              )
              if (is_label_in_labels_to_add) {
                let label_to_add = is_label_in_labels_to_add
                selected_label.id = label_to_add.id
              } else {
                if (!selected_label.id) { //&& !this.labels_to_add.find(l => l.name == selected_label.name && l.start_offset == selected_label.start_offset)
                  let selected_clone = JSON.parse(JSON.stringify(selected_label))
                  this.labels_to_add.push(selected_label)

                  selected_clone.resourcetype = "AudioRegionLabel"
                }
              }
            }
        )*/
        Promise.all(promises).then(() => {
          editedAnnotation['labels'] = this.selected_labels.map(l => l.id)
          AnnotationService.updateAnnotation(vm.annotation.id, editedAnnotation)
              .then(() => {
                this.validationError = ""
              })
              .catch((error) => {
                console.log(JSON.stringify(error))
              })
        })
      }
    },
    submitting: function () {
      let vm = this
      if (vm.submitting) {
        var editedAnnotation = {}
        Object.assign(editedAnnotation, vm.annotation)
        editedAnnotation['is_done'] = true
        editedAnnotation['labels'] = vm.selected_labels.map(l => l.id)
        editedAnnotation['time'] = vm.time
        if (editedAnnotation.has_qa_invalidated) {
          editedAnnotation.is_resubmitted = true
        }
        AnnotationService.updateAnnotation(vm.annotation.id, editedAnnotation)
            .then(
                () => {
                  this.validationError = ""
                  vm.$emit('submitted')
                }
            )
            .catch(error => {
              this.validationError = error.response.data.non_field_errors[0]
              vm.$emit('submiterror')
            })
      }
    },

  },
}
</script>

<style lang="scss">

.task-form-container {
  margin-bottom: 15px;
}

#region-info {
  border: 1px solid lightgrey;
  padding: 10px;
  margin-bottom: 20px;
}

.current-labels {
  display: flex;
  flex-flow: wrap;

  > div {
    margin-right: 5px;
  }

}
</style>
