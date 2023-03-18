<template>
  <div>
    The Sortable list <br>
    Tasks: <br>{{tasks}}
    <br>
    value: {{value}}
    <br>
    sorted tasks: {{sorted_tasks}}
    <draggable
      v-model="sorted_tasks"
      v-bind="dragOptions"
    >
      <transition-group>
        <div v-for="task in sorted_tasks" :key="task.id">
            {{task.name}}
        </div>
    </transition-group>
    </draggable>
  </div>
</template>

<script>
import draggable from 'vuedraggable';

export default {
  name: "ProjectTaskSorter",
  components: {
    draggable,
  },
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  created(){
    console.log("&value", this.value)
  },
  computed: {
    dragOptions() {
      return {
        animation: 300,
        group: 'other',
        disabled: this.readOnly,
        'ghost-class': 'ghost',
      };
    },
  },
  data(){
    return {
      tasks: this.value,
      sorted_tasks: JSON.parse(JSON.stringify(this.value))
    }
  },
  /*watch: {
    tasks: {
      deep: true,
      handler(){
        this.$emit('change')
      },
    },
  },*/
}
</script>

<style scoped>

</style>