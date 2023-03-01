<template>
  <div>
    <h4>Lexicon: {{ lexicon.name }}</h4>
    <div v-if="lexicon">
      <div>
        <v-btn v-if="!adding" @click="adding = true"> Add </v-btn>
        <div v-if="adding" id="adding-form">
          <v-text-field v-model="addedName"> </v-text-field>
          <v-btn @click="add()"> Confirm </v-btn>
        </div>
      </div>
      <v-simple-table>
        <thead>
          <tr>
            <th class="text-left">Entry</th>
            <th class="text-left"></th>
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

      <div v-if="!lexicon.entries.length">No entries</div>
    </div>
  </div>
</template>

<script>
import LexiconService from '@/services/lexicon.service';
import LexiconEntryService from '@/services/lexiconentry.service';

export default {
  name: 'Lexicon',
  props: ['id'],
  data() {
    return {
      lexicon: null,
      adding: false,
      addedName: '',
    };
  },
  created() {
    this.getLexicon();
  },
  methods: {
    getLexicon() {
      LexiconService.get(this.id).then(res => {
        this.lexicon = res.data;
      });
    },
    add() {
      LexiconEntryService.create({
        entry: this.addedName,
        lexicon: this.lexicon.id,
      }).then(() => {
        this.getLexicon();
        this.addedName = '';
        this.adding = false;
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
