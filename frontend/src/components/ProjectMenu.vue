<template>
  <div>
    <v-menu
      open-on-hover
      offset-y
      :close-on-content-click="false"
      :close-on-click="false"
    >
      <template #activator="{ attrs, on: menu }">
        <span v-bind="attrs" v-on="menu">
          <v-icon>mdi-dots-vertical</v-icon>
        </span>
      </template>
      <v-card>
        <v-list>
          <v-list-item @click="toggleArchived">
            {{ archiveAction }}
          </v-list-item>
          <v-list-item @click="$emit('edit', project)">
            {{ $t('Edit') }}
          </v-list-item>
        </v-list>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
import ProjectService from '@/services/project.service.js';

export default {
  name: 'ProjectMenu',
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      project: this.value,
    };
  },
  computed: {
    archiveAction() {
      if (this.project.archived) {
        return this.$t('Unarchive');
      }
      return this.$t('Archive');
    },
  },
  watch: {
    project: {
      deep: true,
      handler() {
        this.$emit('input', this.project);
      },
    },
  },
  methods: {
    toggleArchived() {
      ProjectService.updateProject(this.project.id, {
        archived: !this.project.archived,
      }).then(() => {
        this.project.archived = !this.project.archived;
      });
    },
  },
};
</script>

<style scoped></style>
