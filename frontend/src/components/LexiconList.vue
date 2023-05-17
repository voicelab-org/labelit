<template>
  <div>
    <div class="d-flex justify-space-between align-center">
      <h2 class="headline">{{ $t('Lexicons') }}</h2>
      <v-dialog v-model="dialog" persistent max-width="800px">
        <template #activator="{ on, attrs }">
          <v-btn color="primary" dark v-bind="attrs" v-on="on">
            {{ $t('Add a lexicon') }}
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">{{ $t('Add a lexicon') }}</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-text-field
                v-model="newLexiconName"
                :label="$t('Lexicon name')"
              ></v-text-field>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialog = false">
              {{ $t('Close') }}
            </v-btn>
            <v-btn color="primary" @click="add()">{{ $t('Add') }}</v-btn>
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
      <v-simple-table v-if="lexicons.length">
        <thead>
          <tr>
            <th class="text-left">{{ $t('Lexicon name') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(lexicon, i) in lexicons" :key="i" @click="goTo(lexicon)">
            <td>{{ lexicon.name }}</td>
          </tr>
        </tbody>
      </v-simple-table>
      <div v-else class="text-center">{{ $t('No lexicon') }}</div>
    </div>
  </div>
</template>

<script>
import LexiconService from '@/services/lexicon.service.js';

export default {
  name: 'LexiconList',
  data() {
    return {
      lexicons: [],
      dialog: false,
      loading: true,
      newLexiconName: '',
    };
  },
  created() {
    this.getList();
  },
  methods: {
    add() {
      LexiconService.create({
        name: this.newLexiconName,
      })
        .then(() => {
          this.getList();
        })
        .finally(() => {
          this.dialog = false;
        });
    },
    getList() {
      LexiconService.getList()
        .then(res => {
          this.lexicons = res.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    goTo(lexicon) {
      this.$router.push('lexicon/' + lexicon.id);
    },
  },
};
</script>
