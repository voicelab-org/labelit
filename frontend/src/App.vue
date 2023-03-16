<template>
  <div>
    <BlueFilterOverlay> </BlueFilterOverlay>
    <v-app id="inspire">
      <v-app-bar app color="white" flat>
        <v-container class="py-0 fill-height">
          <img src="/logo_le_voice_lab.png" style="height: 32px" />

          <template v-if="user">
            <v-btn v-if="user.is_staff" to="/dashboard" plain rounded>
              Dashboard
            </v-btn>

            <v-btn to="/projects" plain rounded> Projects </v-btn>
            <v-btn v-if="user.is_staff" to="/datasets" plain rounded>
              Datasets
            </v-btn>
            <v-btn v-if="user.is_staff" to="/tasks" plain rounded>
              Tasks
            </v-btn>
            <v-btn v-if="user.is_staff" to="/lexicons" plain rounded>
              Lexicons
            </v-btn>
          </template>
          <v-spacer></v-spacer>
          <div v-if="user" id="user-corner">
            <BlueFilter />
            <v-btn text :title="user.email" @click="logout()">
              <v-icon>mdi-logout</v-icon>
            </v-btn>
          </div>
          <div v-else>
            <v-btn text :to="{ name: 'login' }">Login</v-btn>
          </div>
        </v-container>
      </v-app-bar>
      <v-main class="grey lighten-3">
        <v-container>
          <v-row>
            <v-col>
              <v-sheet rounded="lg" class="container">
                <router-view></router-view>
              </v-sheet>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
      <labelit-snackbar></labelit-snackbar>
    </v-app>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import BlueFilter from '@/components/BlueFilter.vue';
import BlueFilterOverlay from '@/components/BlueFilterOverlay.vue';
import LabelitSnackbar from '@/components/LabelitSnackbar.vue';

export default {
  name: 'App',
  components: {
    BlueFilter,
    BlueFilterOverlay,
    LabelitSnackbar,
  },
  data: () => ({
    links: ['Projects', 'Datasets'],
  }),
  computed: {
    ...mapGetters({
      user: 'auth/user',
    }),
  },
  methods: {
    logout() {
      this.$store.dispatch('auth/logout');
    },
  },
};
</script>

<style lang="scss">
@import '@/styles/app.scss';

#user-corner {
  display: flex;
  align-items: center;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /*margin-top: 60px;*/
}

#header {
  border-bottom: 1px solid lightgrey;
  height: 50px;
  max-height: 50px;

  > a {
    text-decoration: none;
    color: #2c3e50;
  }

  a img {
    width: 35px;
    height: 35px;
  }

  display: flex;
  align-items: center;
  //justify-content: space-around;
  margin-bottom: 30px;

  #home-link {
    margin-left: 5px;
    display: flex;
    align-items: center;
    width: 110px;
    justify-content: space-between;

    > span {
      text-decoration: none;
      font-size: 20px;
    }
  }
}

#app div {
  margin-bottom: 20px;
}

.label-pill {
  border-radius: 50%;
  height: 11px;
  width: 11px;
  display: inline-block;
  border: 1px solid white;
  height: 31px;
  left: -14px;
  position: relative;
  width: 32px;
}

tr {
  cursor: pointer;

  &.no-click {
    cursor: default;
  }
}

.v-sheet.container {
  padding: 30px;
}

.header {
  margin-bottom: 30px;
}

.v-tabs {
  margin-bottom: 20px;
}

// TODO: check use of the commented lines below
/*
.container {
  width: 1000px !important;
}
*/

//

.stats-table {
  font-family: Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

.stats-table td,
.stats-table th {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;

  &.left {
    text-align: left;
  }
}

.stats-table td:nth-child(2) {
  display: flex;
  justify-content: center;
}

.stats-table th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: center;
  background-color: #03a9f4;
  color: white;
}

.stats-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.stats-table tr:hover {
  background-color: #ddd;
}
</style>
