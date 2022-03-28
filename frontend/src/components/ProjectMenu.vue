<template>
  <div>
    <v-menu
        open-on-hover
        offset-y
    >
      <template v-slot:activator="{ on }">
            <span v-on="on" @click.stop>
                <v-icon>mdi-dots-vertical</v-icon>
            </span>
      </template>
      <v-card>
        <v-list>
          <v-list-item>
            <a @click="toggleArchived"> {{archiveAction}} </a>
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>
  </div>
</template>

<script>

import ProjectService from "@/services/project.service";

export default {
  name: "ProjectMenu",
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      project: this.value,
    }
  },
  computed: {
    archiveAction(){
      if (this.project.archived) {
        return "Unarchive"
      }
      return "Archive"
    },
  },
  watch: {
    project: {
      deep: true,
      handler() {
        this.$emit('input', this.project)
      },
    },
  },
  methods: {
    toggleArchived(){
      ProjectService.updateProject(
          this.project.id,
          {
            archived: !this.project.archived
          }
      ).then(()=>{

        this.project.archived = !this.project.archived
      })
    },
  },
}
</script>

<style scoped>

</style>