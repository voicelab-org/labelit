<template>
 <div class="bg-blue-800 p-4">
   YOYO {{$route.matched}}
        <span v-for="(matched, idx) in $route.matched"
        :key="idx">
        <a
        :href="matched.path">
        {{ matched.name }}
        </a>
        <span v-if="idx != Object.keys($route.matched).length - 1"> / </span>
        </span>

  </div>
</template>

<script>
export default {
  name: "Breadcrumbs"
}
</script>

<style scoped>

</style>