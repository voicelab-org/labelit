<template>
  <div>
    <v-dialog
        v-model="dialog"
        persistent
        max-width="800px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            color="primary"
            dark
            v-bind="attrs"
            v-on="on"
        >
          Add Project
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="headline">Create Project</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-form v-model="valid">
              <v-jsf v-model="model" :schema="schema"/>
            </v-form>
            <p>valid=</p>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              color="blue darken-1"
              text
              @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
              color="blue darken-1"
              text
              @click="create"
          >
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import VJsf from '@koumoul/vjsf/lib/VJsf.js'
import '@koumoul/vjsf/lib/VJsf.css'

export default {
  name: "BatchCreate",
  props: {},
  components: {
    VJsf
  },
  data() {
    return {
      dialog: false,
      //VJSF
      valid: false,
      model: {},
      schema: {
        type: 'object',
        properties: {
          name: {type: 'string',}, // default: "yo"
          is_audio_annotated: {type: 'boolean', default: true,},
          is_text_annotated: {type: 'boolean', default: true},
          // are_sequences_annotated
          timer_inactivity_threshold: {type: 'integer', default: 60000},
          do_display_timer_time: {type: 'boolean', default: false},
          does_audio_playing_count_as_activity: {type: 'boolean', default: true},
          target_num_documents: {type: 'integer', default: 100},
          target_deadline: {
            type: 'string',
            title: 'Target date',
            format: 'date',
          },
          description: {
            type: 'string',
            'x-display': 'textarea'
          },
          tasks: {
            type: 'array',
            title: 'All tasks in this project',
            'x-fromUrl': '/data-fair/api/v1/datasets?status=finalized&select=title,schema&owner={context.owner.type}:{context.owner.id}',
            'x-itemsProp': 'tasks',
            'x-itemTitle': 'name',
            'x-itemKey': 'id',
            items: {
              type: 'object',
              properties: {
                id: {
                  type: 'integer'
                },
                title: {
                  name: 'string'
                }
              }
            }
          },
        }
      },
      //END VJSF'
    }
  },
  methods: {
    create() {
    },
  },
  watch: {}
}
</script>