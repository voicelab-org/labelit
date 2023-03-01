<template>
  <div>
    <template v-if="create_mode">
      <v-btn color="primary" dark @click.stop="show_dialog = true">
        Add Task
      </v-btn>
    </template>
    <v-dialog v-model="show_dialog" max-width="800px" persistent>
      <v-card>
        <v-card-title>
          <span class="headline">
            {{ dialog_title }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-form v-model="valid">
              <v-jsf v-model="model" :schema="schema" :options="form_options" />
            </v-form>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="show_dialog = false">
            Close
          </v-btn>
          <v-btn color="blue darken-1" text :disabled="!valid" @click="submit">
            <span v-if="create_mode">Create</span>
            <span v-else>Update</span>
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import VJsf from '@koumoul/vjsf/lib/VJsf.js';
import '@koumoul/vjsf/lib/VJsf.css';
import TaskService from '@/services/task.service.js';
import ApiService from '@/services/api.service.js';
import LabelService from '@/services/label.service.js';
import CategoricalTaskSchema from '@/components/task_types/task_manager_schemas/CategoricalTaskSchema.json';
import TaskSchemas from '@/components/task_types/task_manager_schemas/index.js';

console.log('schemas:', TaskSchemas);

let resourcetype_choices = Object.keys(TaskSchemas).map(schema_name => {
  return {
    const: schema_name.replace('Schema', ''),
    title: schema_name.replace('Schema', '').split('Task')[0] + ' task',
  };
});
console.log('resourcetype_choices', resourcetype_choices);

export default {
  name: 'TaskManager',
  components: {
    VJsf,
  },
  props: {
    task: {
      type: Object,
      default() {
        return {};
      },
    },
    value: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      TaskSchemas: TaskSchemas,
      CategoricalTaskSchema: CategoricalTaskSchema,
      show_dialog: this.show,
      create_mode: false,
      //VJSF
      valid: false,
      model: this.task,
      form_options: {
        httpLib: ApiService,
        // editMode: 'inline',
      },
      schema: null,
      base_schema: {
        type: 'object',
        required: ['name'],
        properties: {
          name: {
            type: 'string',
          },
          can_documents_be_invalidated: { type: 'boolean', default: true },
          resourcetype: {
            type: 'string',
            title: 'Task type',
            oneOf: Object.keys(TaskSchemas).map(schema_name => {
              return {
                const: schema_name.replace('Schema', ''),
                title:
                  schema_name.replace('Schema', '').split('Task')[0] + ' task',
              };
            }),
          },
        },
      },
      //END VJSF'
    };
  },
  computed: {
    dialog_title() {
      if (this.create_mode) {
        return 'Create a task';
      }
      return 'Edit task ' + this.model.name;
    },
  },
  watch: {
    show_dialog() {
      this.$emit('input', this.show_dialog);
    },
    value() {
      this.show_dialog = this.value;
    },
    task() {
      console.log('task', JSON.parse(JSON.stringify(this.task)));
      let schema = this.TaskSchemas[this.task.resourcetype + 'Schema'];
      this.schema.properties = {
        ...this.base_schema.properties,
        ...schema,
      };
      this.model = this.task;
    },
    'model.resourcetype'() {
      let schema = this.TaskSchemas[this.model.resourcetype + 'Schema'];

      this.schema.properties = {
        ...this.base_schema.properties,
        ...schema,
      };
    },
  },
  created() {
    this.create_mode = Object.keys(this.model).length == 0;
    this.schema = { ...this.base_schema };
  },
  methods: {
    submit() {
      if (this.create_mode) {
        this.create();
      } else {
        this.edit();
      }
    },
    editLabels(labels, task_type) {
      let promises = [];
      labels.forEach(l => {
        let label_type = task_type.replace('Task', 'Label');
        //hack
        if (label_type == 'CategoricalLabel') {
          label_type = 'Label';
        }
        //end hack
        let label_payload = {
          resourcetype: label_type,
        };
        let label_keys = Object.keys(l).filter(k => k[0] != '_');
        label_keys.forEach(k => {
          label_payload[k] = l[k];
        });
        promises.push(
          LabelService.update(label_payload.id, label_payload).then(r => {
            return r.data.id;
          })
        );
      });
      return promises;
    },
    createLabels(labels, task_type) {
      let promises = [];
      labels.forEach(l => {
        let label_type = task_type.replace('Task', 'Label');
        //hack
        if (label_type == 'CategoricalLabel') {
          label_type = 'Label';
        }
        //end hack
        let label_payload = {
          resourcetype: label_type,
        };
        let label_keys = Object.keys(l).filter(k => k[0] != '_');
        label_keys.forEach(k => {
          label_payload[k] = l[k];
        });
        promises.push(
          LabelService.create(label_payload).then(r => {
            return r.data.id;
          })
        );
      });
      return promises;
    },
    create() {
      let t = { ...this.model };

      console.log('t.labels', t.labels);
      let schema = TaskSchemas[t.resourcetype + 'Schema'];
      console.log('&schema keys', Object.keys(schema));
      let promises = [];
      if (Object.keys(this.schema.properties).includes('labels')) {
        console.log('labels in schema');
        promises = this.createLabels(t.labels, t.resourcetype);
      } else {
        console.log('labels not in schema');
      }
      Promise.all(promises).then(ids => {
        console.log('label ids', ids);
        let task_payload = {
          resourcetype: t.resourcetype,
          //name: this.model.name,
          //can_documents_be_invalidated: this.model.can_documents_be_invalidated,
        };
        Object.keys(this.schema.properties).forEach(schema_key => {
          console.log('schema_key', schema_key);
          if (schema_key == 'labels') return;
          task_payload[schema_key] = this.model[schema_key];
        });
        if (Object.keys(schema).includes('labels')) {
          task_payload = {
            labels: ids,
            ...task_payload,
          };
        }

        TaskService.createTask(task_payload).then(() => {
          this.show_dialog = false;
          this.model = {};
          this.$emit('changed');
        });
      });
    },
    edit() {
      let t = { ...this.model };

      let create_labels_promises = [];
      let edit_labels_promises = [];
      if (Object.keys(this.schema.properties).includes('labels')) {
        let labels_to_create = t.labels.filter(l => {
          return l.id == null;
        });

        let labels_to_keep = t.labels.filter(l => l.id != null);

        create_labels_promises = this.createLabels(
          labels_to_create,
          t.resourcetype
        );
        edit_labels_promises = this.editLabels(labels_to_keep, t.resourcetype);
      }

      Promise.all(create_labels_promises.concat(edit_labels_promises)).then(
        label_ids => {
          /*
            let task_payload = {
              resourcetype: t.resourcetype,
              //name: this.model.name,
              //can_documents_be_invalidated: this.model.can_documents_be_invalidated,
            }
            Object.keys(this.schema.properties).forEach(
                (schema_key) => {
                  console.log("schema_key", schema_key)
                  if (schema_key == "labels") return
                  task_payload[schema_key] = this.model[schema_key]
                }
            )
            if ("labels" in Object.keys(schema)) {
              task_payload = {
                labels: ids,
                ...task_payload
              }
            }
             */

          let task_payload = {
            id: this.task.id,
            resourcetype: t.resourcetype,
          };
          if (Object.keys(this.schema.properties).includes('labels')) {
            task_payload = {
              labels: label_ids,
              ...task_payload,
            };
          }
          Object.keys(this.schema.properties).forEach(schema_key => {
            console.log('schema_key', schema_key);
            if (schema_key == 'labels') return;
            task_payload[schema_key] = this.model[schema_key];
          });
          TaskService.updateTask(this.task.id, task_payload).then(() => {
            this.show_dialog = false;
            this.model = {};
            this.$emit('changed');
          });
        }
      );
    },
  },
};
</script>
