<template>
  <div class="task-form-container">
    <TaskFormHeader :task="task" :read-only="readOnly" />
    <br />
    <div v-if="!readOnly" id="entity-info">
      Highlight entities in the text displayed above.
    </div>
    <span v-show="false"> Selected labels: {{ selected_labels }} </span>
    <!--HACK,  TODO: understand why it breaks after removing this line-->

    <div v-if="readOnly">
      <v-checkbox v-model="showAnnotatedEntities">
        <div slot="label">Show annotations</div>
      </v-checkbox>
    </div>

    <div>
      <div
        v-for="(val, key) in grouped_selected_labels"
        :key="key"
        style="margin-bottom: 5px"
      >
        <v-chip pill small :color="val[0].color" text-color="white">
          {{ grouped_selected_labels[key].length }}
        </v-chip>
        {{ key }}
      </div>
    </div>
  </div>
</template>
<script>
import TaskForm from '@/components/mixins/TaskForm.vue';
import TaskFormHeader from '@/components/TaskFormHeader.vue';
import { mapGetters } from 'vuex';
import AnnotationService from '@/services/annotation.service.js';
import LabelService from '@/services/label.service.js';

export default {
  name: 'EntityTaskForm',
  components: {
    TaskFormHeader,
  },
  mixins: [TaskForm],
  computed: {
    ...mapGetters({
      entity_tasks: 'entities/entity_tasks',
      annotated_entities: 'entities/annotated_entities',
    }),
    grouped_selected_labels() {
      if (!this.annotated_entities.length) {
        return {};
      }
      let grouped = this.groupBy(this.selected_labels, 'name');
      return grouped;
    },
  },
  watch: {
    showAnnotatedEntities() {
      if (this.showAnnotatedEntities) {
        this.$store.commit(
          'entities/SET_ANNOTATED_ENTITIES',
          this.selected_labels
        );
      } else {
        this.$store.commit('entities/SET_ANNOTATED_ENTITIES', []);
      }
    },
    annotated_entities() {
      if (this.readOnly) return;
      this.selected_labels = this.annotated_entities.filter(e => {
        return e.task == this.task.id;
      });
    },
    selected_labels: {
      deep: true,
      handler() {
        let vm = this;
        var editedAnnotation = {};
        Object.assign(editedAnnotation, vm.annotation);
        let promises = [];
        this.selected_labels.forEach(selected_label => {
          let is_label_in_labels_to_add = this.labels_to_add.find(
            l =>
              l.name == selected_label.name &&
              l.start_offset == selected_label.start_offset &&
              l.end_offset == selected_label.end_offset
          );
          if (is_label_in_labels_to_add) {
            selected_label.id = is_label_in_labels_to_add.id;
          } else {
            if (!selected_label.id) {
              //&& !this.labels_to_add.find(l => l.name == selected_label.name && l.start_offset == selected_label.start_offset)
              let selected_clone = JSON.parse(JSON.stringify(selected_label));
              this.labels_to_add.push(selected_label);

              let original_label = this.entity_tasks
                .find(t => t.id == selected_label.task)
                .labels.find(l => l.name == selected_label.name);

              selected_clone.source_label = original_label.id;

              selected_clone.resourcetype = 'EntityLabel';
              promises.push(
                LabelService.create(selected_clone).then(res => {
                  selected_label.id = res.data.id;
                })
              );
            }
          }
        });
        Promise.all(promises).then(() => {
          editedAnnotation['labels'] = this.selected_labels.map(l => l.id);
          AnnotationService.updateAnnotation(vm.annotation.id, editedAnnotation)
            .then(() => {
              this.validationError = '';
            })
            .catch(error => {
              console.error(JSON.stringify(error));
            });
        });
      },
    },
    submitting: function () {
      let vm = this;
      if (vm.submitting) {
        var editedAnnotation = {};
        Object.assign(editedAnnotation, vm.annotation);
        editedAnnotation['is_done'] = true;
        editedAnnotation['labels'] = vm.selected_labels.map(l => l.id);
        editedAnnotation['time'] = vm.time;
        if (editedAnnotation.has_qa_invalidated) {
          editedAnnotation.is_resubmitted = true;
        }
        AnnotationService.updateAnnotation(vm.annotation.id, editedAnnotation)
          .then(() => {
            this.validationError = '';
            vm.$emit('submitted');
          })
          .catch(error => {
            this.validationError = error.response.data.non_field_errors[0];
            vm.$emit('submiterror');
          });
      }
    },
  },
  created() {
    this.$store.commit('entities/ADD_TASK', this.task);

    let selected_labels = [];
    let promises = [];
    this.annotation.labels.forEach(id => {
      promises.push(
        LabelService.get(id).then(res => selected_labels.push(res.data))
      );
    });
    Promise.all(promises).then(() => {
      this.selected_labels = selected_labels;
      if (!this.readOnly) {
        this.$store.commit(
          'entities/ADD_ANNOTATED_ENTITIES',
          this.selected_labels
        );
      }
    });
  },
  data() {
    return {
      labels_to_add: [],
      showAnnotatedEntities: false,
      isMixinWatcherActive: false,
    };
  },
  methods: {
    groupBy(xs, key) {
      return xs.reduce(function (rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
      }, {});
    },
  },
};
</script>

<style>
.task-form-container {
  margin-bottom: 15px;
}

#entity-info {
  border: 1px solid lightgrey;
  padding: 10px;
  margin-bottom: 20px;
}
</style>
