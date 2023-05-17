<template>
  <div id="dashboard">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      links: [
        {
          name: 'Stats',
          dest: '/dashboard/stats/',
        },
        {
          name: 'Projects',
          dest: '/dashboard/projects/',
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
