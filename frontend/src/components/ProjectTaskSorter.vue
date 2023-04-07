<template>
  <div>
    <p>
      Define the order of presentation of the tasks (you can drag the items)
    </p>
    <div>

      <draggable
          v-model="sorted_tasks"
      >
        <transition-group>
          <div
              v-for="task in sorted_tasks"
              :key="task.id"
              class="ordered-task"
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
      dummy: [],
    }
  },
  watch: {
    value: {
      deep: true,
      handler() {

        let vm = this

        function _sets_differ() {
          let value_set = new Set(vm.value)
          let sorted_task_set = new Set(vm.sorted_tasks)
          return value_set !== sorted_task_set
        }

        function _edit_sorted_tasks() {
          function _remove_detached_tasks() {
            vm.sorted_tasks = vm.sorted_tasks.filter(t => !vm.value.includes(t))
          }

          function _add_new_tasks() {

            let tasks_to_add = vm.value.filter(t => !vm.sorted_tasks.map(t => t.id).includes(t.id))
            tasks_to_add.forEach(
                (t) => {
                  vm.sorted_tasks.push(t)
                }
            )
          }

          _remove_detached_tasks()
          _add_new_tasks()

          return vm.sorted_tasks

        }

        if (_sets_differ()) {

          let sorted_tasks = _edit_sorted_tasks()
          this.sorted_tasks = sorted_tasks
        }
      },
    },
    sorted_tasks: {
      handler() {
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
          this.$emit('input', this.sorted_tasks)
        }
      },
    }
  },
}
</script>

<style scoped lang="scss">

.ordered-task {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-top: 1px solid lightgrey;
  cursor: grab;
}

</style>