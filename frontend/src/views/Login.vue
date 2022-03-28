<template>
  <v-layout text-center wrap>

    <span v-shortkey="['enter']" @shortkey="handleLogin"></span>
    <v-flex xs12>
      <v-img
        :src="require('../assets/logo_le_voice_lab.png')"
        class="my-3"
        contain
        height="150"
      ></v-img>
    </v-flex>
    <v-card width="400" class="mx-auto mt-5">
      <v-card-title>
        <h1 class="display-7">Login</h1>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            label="Email"
            v-model="user.email"
            prepend-icon="mdi-account-circle"
          />
          <v-text-field
            :type="showPassword ? 'text' : 'password'"
            label="Password"
            prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
            v-model="user.password"
          />
        </v-form>
      </v-card-text>
      <v-divider></v-divider>
      <template v-if="message">
        <v-card-text>
          Could not login. Did you enter the correct username and password ?
        </v-card-text>
      </template>
      <v-card-actions class="card-Action">
        <v-btn class="loginBtn" color="info" @click="handleLogin">Login</v-btn>
      </v-card-actions>
    </v-card>
  </v-layout>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: "LoginPage",
  data() {
    return {
      user: { email: "", password: "" },
      loading: false,
      message: "",
      showPassword: false
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn
    },
  },
  methods: {
    ...mapActions('auth', ['authenticateUser']),
    handleLogin() {
      this.loading = true;
      if (this.user.email && this.user.password) {
        this.authenticateUser(this.user).then(
          () => {
            this.$router.push("/projects");
          },
          error => {
            this.loading = false;
            this.message =
              (error.response && error.response.data) ||
              error.message ||
              error.toString();
            console.log("msg", this.message)
          }
        );
      }
    }
  }
};
</script>

<style scoped>
.card-Action {
  position: relative;
}

.loginBtn {
  position: relative;
  left: 40%;
}
</style>
