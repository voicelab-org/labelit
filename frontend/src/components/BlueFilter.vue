<template>
  <v-menu
    v-model="menu"
    :close-on-content-click="false"
    offset-y
    :nudge-width="200"
  >
    <template #activator="{ on, attrs }">
      <v-btn text v-bind="attrs" v-on="on">
        <v-icon :color="'orange'">mdi-weather-night</v-icon>
        <span
          >&nbsp;{{
            percentage.toLocaleString('en-US', {
              minimumIntegerDigits: 2,
              useGrouping: false,
            })
          }}
          %</span
        >
      </v-btn>
    </template>
    <v-card>
      <v-card-text>
        <div class="text-caption"> {{$t('Blue filter')}} :</div>
        <v-slider
          height="60px"
          :value="percentage"
          :hide-details="true"
          :color="'orange'"
          :track-color="'blue'"
          @change="updatePercentage"
        ></v-slider>
      </v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'BlueFilter',
  data: () => ({
    menu: false,
  }),
  computed: {
    ...mapGetters({
      percentage: 'blueFilter/percentage',
    }),
  },
  methods: {
    updatePercentage(value) {
      this.$store.commit('blueFilter/SET_PERCENTAGE', parseInt(value));
    },
  },
};
</script>
