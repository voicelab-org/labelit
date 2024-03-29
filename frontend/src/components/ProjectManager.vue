<template>
  <div>
    <template v-if="create_mode">
      <v-btn color="primary" dark @click.stop="show_dialog = true">
        {{ $t('Add project') }}
      </v-btn>
    </template>
    <v-dialog
      v-model="show_dialog"
      max-width="800px"
      persistent
      @input="dialogInputEvent"
    >
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

            <template v-if="model.tasks && model.tasks.length">
              <ProjectTaskSorter v-model="model.tasks" />
            </template>
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
import ProjectService from '../services/project.service.js';
import ApiService from '../services/api.service.js';
import ProjectTaskSorter from './ProjectTaskSorter.vue';

export default {
  name: 'ProjectManager',
  components: {
    VJsf,
    ProjectTaskSorter,
  },
  props: {
    project: {
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
      show_dialog: this.show,
      create_mode: false,
      //VJSF
      valid: false,
      model: this.project,
      form_options: {
        httpLib: ApiService,
      },
      schema: {
        // would be nice if the backend could automagically generate this schema
        type: 'object',
        required: ['name', 'target_deadline', 'target_num_documents'],
        properties: {
          name: {
            type: 'string',
            title: this.$t('name'),
          },
          is_audio_annotated: {
            type: 'boolean',
            default: true,
            title: this.$t('projectForm.is_audio_annotated'),
          },
          is_video_annotated: {
            type: 'boolean',
            default: false,
            title: this.$t('projectForm.is_video_annotated'),
          },
          enable_region_annotation: {
            type: 'boolean',
            default: false,
            title: this.$t('projectForm.enable_region_annotation'),
          },
          is_text_annotated: {
            type: 'boolean',
            default: true,
            title: this.$t('projectForm.is_text_annotated'),
          },
          timer_inactivity_threshold: {
            type: 'integer',
            default: 60000,
            title: this.$t('projectForm.timer_inactivity_threshold'),
          },
          do_display_timer_time: {
            type: 'boolean',
            default: false,
            title: this.$t('projectForm.do_display_timer_time'),
          },
          does_audio_playing_count_as_activity: {
            type: 'boolean',
            default: true,
            title: this.$t('projectForm.does_audio_playing_count_as_activity'),
          },
          task_presentation: {
            type: 'string',
            default: 'list',
            title: this.$t('projectForm.task_presentation'),
            //title:'How to present the tasks to the annotator(s): as a list or as a sequence',
          },
          target_num_documents: {
            type: 'integer',
            default: 100,
            title: this.$t('projectForm.target_num_documents'),
          },
          target_deadline: {
            type: 'string',
            //title: 'Target date',
            format: 'date',
            title: this.$t('projectForm.target_deadline'),
          },
          description: {
            type: 'string',
            'x-display': 'textarea',
            title: this.$t('projectForm.description'),
          },
          tasks: {
            type: 'array',
            //title: 'All tasks in this project',
            title: this.$t('projectForm.tasks'),
            'x-fromUrl': '/tasks/',
            'x-itemTitle': 'name',
            'x-itemKey': 'id',
            items: {
              type: 'object',
              properties: {
                id: {
                  type: 'integer',
                },
                name: {
                  type: 'string',
                },
              },
            },
          },
        },
      },
      //END VJSF'
    };
  },
  computed: {
    dialog_title() {
      if (this.create_mode) {
        return this.$t('Create a project');
      }
      return this.$t('Edit project') + ' ' + this.model.name;
    },
  },
  watch: {
    show_dialog() {
      this.$emit('input', this.show_dialog);
    },
    value() {
      this.show_dialog = this.value;
    },
    project() {
      this.model = this.project;
    },
  },
  created() {
    this.create_mode = Object.keys(this.model).length == 0;
  },
  methods: {
    dialogInputEvent() {},
    submit() {
      if (this.create_mode) {
        this.create();
      } else {
        this.edit();
      }
    },
    create() {
      let task_ids = this.model.tasks.map(t => t.id);
      let p = {
        ...this.model,
        tasks: task_ids,
      };
      ProjectService.create(p).then(() => {
        this.show_dialog = false;
        this.model = {};
        this.$emit('changed');
      });
    },
    edit() {
      let p = { ...this.model };
      p.tasks = p.tasks.map(t => t.id);
      ProjectService.updateProject(this.project.id, p).then(() => {
        this.show_dialog = false;
        this.model = {};
        this.$emit('changed');
      });
    },
  },
};
</script>
