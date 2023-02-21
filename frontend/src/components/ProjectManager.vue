<template>
  <div>
    <template v-if="create_mode">
      <v-btn color="primary" dark @click.stop="show_dialog = true">
        Add Project
      </v-btn>
    </template>
    <v-dialog
      v-model="show_dialog"
      @input="dialogInputEvent"
      max-width="800px"
      persistent
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
      <!--<div>
        Project mdl: <br>
        {{model}}
      </div>-->
    </v-dialog>
  </div>
</template>

<script>
import VJsf from "@koumoul/vjsf/lib/VJsf.js";
import "@koumoul/vjsf/lib/VJsf.css";
import ProjectService from "../services/project.service";
import ApiService from "../services/api.service";

export default {
  name: "ProjectManager",
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
  components: {
    VJsf,
  },
  computed: {
    dialog_title() {
      if (this.create_mode) {
        return "Create a project";
      }
      return "Edit project " + this.model.name;
    },
  },
  created() {
    this.create_mode = Object.keys(this.model).length == 0;
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
        type: "object",
        required: ["name", "target_deadline", "target_num_documents"],
        properties: {
          name: {
            type: "string",
          },
          is_audio_annotated: { type: "boolean", default: true },
          enable_region_annotation: { type: "boolean", default: false },
          is_text_annotated: { type: "boolean", default: true },
          // are_sequences_annotated
          timer_inactivity_threshold: { type: "integer", default: 60000 },
          do_display_timer_time: { type: "boolean", default: false },
          does_audio_playing_count_as_activity: {
            type: "boolean",
            default: true,
          },
          target_num_documents: { type: "integer", default: 100 },
          target_deadline: {
            type: "string",
            title: "Target date",
            format: "date",
          },
          description: {
            type: "string",
            "x-display": "textarea",
          },
          tasks: {
            type: "array",
            title: "All tasks in this project",
            "x-fromUrl": "/tasks/",
            "x-itemTitle": "name",
            "x-itemKey": "id",
            items: {
              type: "object",
              properties: {
                id: {
                  type: "integer",
                },
                name: {
                  type: "string",
                },
              },
            },
          },
        },
      },
      //END VJSF'
    };
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
      let p = { ...this.model };
      p.tasks = p.tasks.map((t) => t.id);
      ProjectService.create(p).then(() => {
        this.show_dialog = false;
        this.model = {};
        this.$emit("changed");
      });
    },
    edit() {
      let p = { ...this.model };
      p.tasks = p.tasks.map((t) => t.id);
      ProjectService.updateProject(this.project.id, p).then(() => {
        this.show_dialog = false;
        this.model = {};
        this.$emit("changed");
      });
    },
  },
  watch: {
    show_dialog() {
      this.$emit("input", this.show_dialog);
    },
    value() {
      this.show_dialog = this.value;
    },
    project() {
      this.model = this.project;
    },
  },
};
</script>
