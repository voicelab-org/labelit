<template>
  <div id="dashboard">
    <!--
    <v-tabs>
        <v-tab v-for="link in links" :key="link.dest" :to="link.dest">
            {{link.name}}
        </v-tab>
    </v-tabs>
    -->

    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "dashboard",
  data() {
    return {
      links: [
        {
          name: "Stats",
          dest: "/dashboard/stats/",
        },
        {
          name: "Projects",
          dest: "/dashboard/projects/",
        },
      ],
    };
  },
};
</script>

<style scoped lang="scss">
#links {
  display: flex;
  justify-content: center;
  > div {
    margin: 0 15px;
  }
}
</style>
