<template>
  <div>
    <div class="list-actions">
      <v-btn @click="openAdd" color="primary">Add</v-btn>
    </div>
    <div v-if="adding">
      <v-text-field v-model="addedName"/>
      <v-btn @click="add" color="primary">Confirm</v-btn>
    </div>
    <div v-if="lexicons">
      <div v-for="lexicon in lexicons" :key="lexicon.name">
        <router-link :to="'lexicon/'+lexicon.id">{{ lexicon.name }}</router-link>
      </div>
    </div>
  </div>
</template>

<script>

import LexiconService from "@/services/lexicon.service";

export default {
  name: "LexiconList",
  data() {
    return {
      lexicons: null,
      adding: false,
      addedName: '',
    }
  },
  created() {
    this.getList()
  },
  methods: {
    openAdd() {
      this.adding = true
    },
    add() {
      LexiconService.create(
          {
            name: this.addedName
          }
      ).then(() => {
        this.getList()
        this.adding = false
      })
    },
    getList() {
      LexiconService.getList().then((res) => {
        this.lexicons = res.data
      })
    },
  },
}
</script>

<style scoped>
.list-actions{
  margin-bottom: 20px;
}
</style>