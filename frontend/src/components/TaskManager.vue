<template>
  <div>
    <template v-if="create_mode">
      <v-btn
          color="primary"
          dark
          @click.stop="show_dialog=true"
      >
        Add Task
      </v-btn>
    </template>
    <v-dialog
        v-model="show_dialog"
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
              <v-jsf
                  v-model="model"
                  :schema="schema"
                  :options="form_options"
              />
            </v-form>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              color="blue darken-1"
              text
              @click="show_dialog=false"
          >
            Close
          </v-btn>
          <v-btn
              color="blue darken-1"
              text
              :disabled="!valid"
              @click="submit"
          >
            <span v-if="create_mode">Create</span>
            <span v-else>Update</span>
          </v-btn>
        </v-card-actions>
      </v-card>
      <!--<div>
        Task mdl: <br>
        {{model}}
      </div>-->
    </v-dialog>
  </div>
</template>

<script>

import VJsf from '@koumoul/vjsf/lib/VJsf.js'
import '@koumoul/vjsf/lib/VJsf.css'
import TaskService from "../services/task.service";
import ApiService from "../services/api.service";

export default {
  name: "TaskManager",
  props: {
    task: {
      type: Object,
      default() {
        return {}
      },
    },
    value: {
      type: Boolean,
      default: false
    }
  },
  components: {
    VJsf
  },
  computed: {
    dialog_title() {
      if (this.create_mode) {
        return "Create a task"
      }
      return "Edit task " + this.model.name
    }
  },
  created() {
    this.create_mode = Object.keys(this.model).length == 0
  },
  data() {
    return {
      show_dialog: this.show,
      create_mode: false,
      //VJSF
      valid: false,
      model: this.task,
      form_options: {
        httpLib: ApiService
      },
      schema: {
        type: 'object',
        required: [
          'name',
        ],
        properties: {
          name: {
            type: 'string',
          },
          can_documents_be_invalidated: {type: 'boolean', default: true,},
          taskType: {
            type: 'string',
            title: "Task type",
            oneOf: [
              {
                const: 'CategoricalTask',
                title: 'Categorical task',
              },
              {
                const: 'EntityTask',
                title: 'Entity task',
              }
            ]
          }
        }
      },
      //END VJSF'
    }
  },
  methods: {
    submit() {
      if (this.create_mode) {
        this.create()
      } else {
        this.edit()
      }
    },
    create() {
      let p = {...this.model}
      p.tasks = p.tasks.map(t => t.id)
      TaskService.create(p).then(
          () => {
            this.show_dialog = false
            this.model = {}
            this.$emit('changed')
          }
      )
    },
    edit() {
      let p = {...this.model}
      p.tasks = p.tasks.map(t => t.id)
      TaskService.updateTask(this.task.id, p).then(
          () => {
            this.show_dialog = false
            this.model = {}
            this.$emit('changed')
          }
      )
    },
  },
  watch: {
    show_dialog(){
      this.$emit('input', this.show_dialog)
    },
    value(){
      this.show_dialog = this.value
    },
    task(){
      this.model = this.task
    },
  }
}
</script>