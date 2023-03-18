<template>
  <div>
    The Sortable list <br>
    value: {{ value }}
    <br>
    sorted tasks: {{ sorted_tasks }}
    <div><!--:key="draggable_key"-->

      <draggable
          v-model="sorted_tasks"
          :key="draggable_key"
      >
        <transition-group :key="draggable_key + 1">
          <div
              v-for="task in sorted_tasks"
              :key="task.id"
          >
            {{ task.name }}
          </div>
        </transition-group>
      </draggable>
    </div>
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
  data() {
    return {
      sorted_tasks: JSON.parse(JSON.stringify(this.value)),
      //sorted_tasks: this.value,
      draggable_key: 123,
      dummy: [],
    }
  },
  watch: {
    value: {
      deep: true,
      handler() {

        console.log("&in value prop change handler")

        //this.sorted_tasks = [{id: 1, name: "yo"}]

        //return

        /*

        // Examples
        const setA = new Set([1, 2, 3, 4]);
        const setB = new Set([2, 3]);
        const setC = new Set([3, 4, 5, 6]);

        isSuperset(setA, setB); // returns true
        union(setA, setC); // returns Set {1, 2, 3, 4, 5, 6}
        intersection(setA, setC); // returns Set {3, 4}
        symmetricDifference(setA, setC); // returns Set {1, 2, 5, 6}
        difference(setA, setC); // returns Set {1, 2}
         */

        let vm = this

        function _sets_differ() {
          let value_set = new Set(vm.value)
          let sorted_task_set = new Set(vm.sorted_tasks)
          return value_set !== sorted_task_set
        }

        function _edit_sorted_tasks() {
          function _remove_detached_tasks() {
            console.log("&_remove_detached_tasks")
            //vm.$nextTick(() => {
              vm.sorted_tasks = vm.sorted_tasks.filter(t => !vm.value.includes(t))
            //})
          }

          function _add_new_tasks() {
            console.log("&_add_new_tasks")
            console.log("&before: ", JSON.parse(JSON.stringify(vm.sorted_tasks)), JSON.parse(JSON.stringify(vm.value)))

            let tasks_to_add = vm.value.filter(t => !vm.sorted_tasks.map(t => t.id).includes(t.id))
            /*vm.sorted_tasks = vm.sorted_tasks.concat(
                vm.value.filter(t => !vm.sorted_tasks.map(t => t.id).includes(t.id))
            )*/
            tasks_to_add.forEach(
                (t) => {
                  vm.sorted_tasks.push(t)
                }
            )
            console.log("vm.value.filter(t => !vm.sorted_tasks.map(t => t.id).includes(t.id))", vm.value.filter(t => !vm.sorted_tasks.map(t => t.id).includes(t.id)))
            console.log("&after: ", JSON.parse(JSON.stringify(vm.sorted_tasks)), JSON.parse(JSON.stringify(vm.value)))
          }


          _remove_detached_tasks()
          _add_new_tasks()
          //vm.draggable_key++

          return vm.sorted_tasks

        }

        if (_sets_differ()) {

          let sorted_tasks = _edit_sorted_tasks()
          console.log("sorted_tasks", JSON.parse(JSON.stringify(sorted_tasks)))
          this.sorted_tasks = sorted_tasks
          this.draggable_key++
          console.log("&sorted_tasks edited")
        }
      },
    },
    sorted_tasks: {
      handler() {
        console.log("&sorted_task handler", this.sorted_tasks)
        var vm = this

        function _task_sets_match_but_are_ordered_differently() {
          function arrayEquals(a, b) {
            return Array.isArray(a) &&
                Array.isArray(b) &&
                a.length === b.length &&
                a.every((val, index) => val === b[index]);
          }

          let sorted_ids = vm.sorted_tasks.map(t => t.id)
          let value_ids = vm.value.map(t => t.id)
          let sorted_tasks_includes_unique_items = vm.sorted_tasks.length != vm.sorted_tasks.map(t => t.id).filter(t_id => vm.value.map(t => t.id).includes(t_id)).length
          let value_includes_unique_items = vm.value.length != vm.value.map(t => t.id).filter(t_id => vm.sorted_tasks.map(t => t.id).includes(t_id)).length
          let is_order_different = !arrayEquals(sorted_ids, value_ids)


          return !sorted_tasks_includes_unique_items && !value_includes_unique_items && is_order_different
        }

        if (_task_sets_match_but_are_ordered_differently()) {
          console.log('&emitting input evt', JSON.parse(JSON.stringify(this.sorted_tasks)))
          this.$emit('input', this.sorted_tasks)
        }
      },
    }
  },
}
</script>

<style scoped>

</style>