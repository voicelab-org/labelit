<template>
  <v-layout text-center wrap>
    <span v-shortkey="['enter']" @shortkey="handleLogin"></span>
    <v-flex xs12>
      <v-img
        src="/logo_le_voice_lab.png"
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
            v-model="user.email"
            label="Email"
            prepend-icon="mdi-account-circle"
          />
          <v-text-field
            v-model="user.password"
            :type="showPassword ? 'text' : 'password'"
            label="Password"
            prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
          />
        </v-form>
      </v-card-text>
      <v-card-actions class="d-flex justify-center">
        <v-btn
          class="loginBtn"
          color="info"
          :loading="loading"
          @click="handleLogin"
        >
          Login
        </v-btn>
        <div v-if="isDevEnv()">
          <v-btn
            class="loginBtn"
            color="info"
            :loading="loading"
            @click="handleLoginDev('qa@qa.com', 'QApassword')"
          >
            Login QA
          </v-btn>
          <v-btn
            class="loginBtn"
            color="info"
            :loading="loading"
            @click="handleLoginDev('a1@annotator.com', 'a1password')"
          >
            Login A1
          </v-btn>
          <v-btn
            class="loginBtn"
            color="info"
            :loading="loading"
            @click="handleLoginDev('a2@annotator.com', 'a2password')"
          >
            Login A2
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
  </v-layout>
</template>

<script>
import { SNACKBAR_TYPE_COLOR } from '@/store/snackbar.module';
import { mapActions } from 'vuex';
export default {
  name: 'LoginPage',
  data() {
    return {
      user: { email: '', password: '' },
      loading: false,
      message: '',
      showPassword: false,
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
  methods: {
    ...mapActions('auth', ['authenticateUser']),
    ...mapActions('snackbar', ['showSnackbar']),
    handleLogin() {
      this.loading = true;
      if (this.user.email && this.user.password) {
        this.authenticateUser(this.user)
          .then(() => {
            this.showSnackbar({
              type: SNACKBAR_TYPE_COLOR.SUCCESS,
              text: 'Successfully logged in. Good work on LabelIt 🚀',
            });
            this.$router.push('/projects');
          })
          .catch(() => {
            this.showSnackbar({
              type: SNACKBAR_TYPE_COLOR.ERROR,
              text: 'Could not login. Did you enter the correct username and password ?',
            });
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
    handleLoginDev(email, password) {
      this.user = {
        email,
        password,
      };
      this.handleLogin();
    },
    isDevEnv() {
      return import.meta.env.DEV;
    },
  },
};
</script>

<style scoped>
.card-Action {
  position: relative;
}
</style>
