<template>
  <div>
    <div class="d-flex justify-space-between align-center">
      <div class="d-flex align-center">
        <v-btn icon @click="$router.push('/lexicons')">
          <v-icon> mdi-arrow-left </v-icon>
        </v-btn>
        <h2 class="headline">{{$t('Lexicon')}}: {{ lexicon?.name }}</h2>
      </div>
      <v-dialog v-model="dialog" persistent max-width="800px">
        <template #activator="{ on, attrs }">
          <v-btn color="primary" dark v-bind="attrs" v-on="on">
            {{$t('Add an entry')}}
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">
              {{$t('Add an entry')}}
            </span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-text-field
                v-model="newEntryName"
                :label="$t('Entry name')"
              ></v-text-field>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialog = false">
              Close
            </v-btn>
            <v-btn color="primary" @click="add()">{{$t('Add')}}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
    <div v-if="loading" class="d-flex justify-center mt-12">
      <v-progress-circular
        color="blue-grey"
        indeterminate
      ></v-progress-circular>
    </div>
    <div v-else class="mt-12">
      <v-simple-table v-if="lexicon.entries.length">
        <thead>
          <tr>
            <th class="text-left">{{$t('Entry')}}</th>
            <th class="text-left actions-table-column"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in lexicon.entries" :key="entry.id">
            <td>{{ entry.entry }}</td>
            <td>
              <v-btn icon @click="deleteEntry(entry)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-simple-table>
      <div v-else class="text-center">{{$t('No entries')}}</div>
    </div>
  </div>
</template>

<script>
import LexiconService from '@/services/lexicon.service.js';
import LexiconEntryService from '@/services/lexiconentry.service.js';

export default {
  name: 'Lexicon',
  props: ['id'],
  data() {
    return {
      lexicon: null,
      dialog: false,
      newEntryName: '',
      loading: true,
    };
  },
  created() {
    this.getLexicon();
  },
  methods: {
    getLexicon() {
      LexiconService.get(this.id)
        .then(res => {
          this.lexicon = res.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    add() {
      LexiconEntryService.create({
        entry: this.newEntryName,
        lexicon: this.lexicon.id,
      })
        .then(() => {
          this.getLexicon();
        })
        .finally(() => {
          this.newEntryName = '';
          this.dialog = false;
        });
    },
    deleteEntry(entry) {
      LexiconEntryService.delete(entry.id).then(() => {
        this.getLexicon();
      });
    },
  },
};
</script>

<style lang="scss" scoped></style>
