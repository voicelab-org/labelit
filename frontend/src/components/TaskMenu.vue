<template>
  <div>
    <v-menu
      open-on-hover
      offset-y
      :close-on-content-click="false"
      :close-on-click="false"
    >
      <template #activator="{ on }">
        <span v-on="on" @click.stop>
          <v-icon>mdi-dots-vertical</v-icon>
        </span>
      </template>
      <v-card>
        <v-list>
          <v-list-item @click="toggleArchived">
            {{ archiveAction }}
          </v-list-item>
          <v-list-item @click="$emit('edit', task)"> Edit </v-list-item>
        </v-list>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
import TaskService from '@/services/task.service.js';

export default {
  name: 'TaskMenu',
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      task: this.value,
    };
  },
  computed: {
    archiveAction() {
      if (this.task.archived) {
        return 'Unarchive';
      }
      return 'Archive';
    },
  },
  watch: {
    task: {
      deep: true,
      handler() {
        this.$emit('input', this.task);
      },
    },
    value: {
      deep: true,
      handler() {
        this.task = this.value;
      },
    },
  },
  methods: {
    toggleArchived() {
      TaskService.updateTask(this.task.id, {
        archived: !this.task.archived,
        resourcetype: this.task.resourcetype,
      }).then(() => {
        this.task.archived = !this.task.archived;
      });
    },
  },
};
</script>

<style scoped></style>
