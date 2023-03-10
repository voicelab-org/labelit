<template>
  <div>
    <v-menu open-on-hover offset-y>
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
        </v-list>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
import BatchService from '@/services/batch.service.js';

export default {
  name: 'BatchMenu',
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      batch: this.value,
    };
  },
  computed: {
    archiveAction() {
      if (this.batch.archived) {
        return 'Unarchive';
      }
      return 'Archive';
    },
  },
  watch: {
    batch: {
      deep: true,
      handler() {
        this.$emit('input', this.batch);
      },
    },
  },
  methods: {
    toggleArchived() {
      BatchService.updateBatch(this.batch.id, {
        archived: !this.batch.archived,
        resourcetype: 'Batch',
      }).then(() => {
        this.batch.archived = !this.batch.archived;
      });
    },
  },
};
</script>

<style scoped></style>
