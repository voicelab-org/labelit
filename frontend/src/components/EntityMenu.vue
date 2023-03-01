<template>
  <div id="entity-menu">
    <v-menu :value="show" :position-x="x" :position-y="y" absolute offset-y>
      <v-list
        :ref="'taskList'"
        dense
        min-width="150"
        max-height="400"
        class="overflow-y-auto"
      >
        <span
          v-shortkey="['enter']"
          @shortkey="$emit('selected', active_label.id)"
        ></span>
        <span v-shortkey="['arrowup']" @shortkey="browseLabels('up')"></span>
        <span
          v-shortkey="['arrowdown']"
          @shortkey="browseLabels('down')"
        ></span>
        <span v-shortkey="['arrowleft']" @shortkey="browseTasks('left')"></span>
        <span
          v-shortkey="['arrowright']"
          @shortkey="browseTasks('right')"
        ></span>

        <v-list v-for="(task, i) in tasks" :key="i" :ref="'task-' + task.id">
          <span :class="{ active: task == active_task }">
            <v-list-item>
              <v-list-item-title>{{ task.name }}</v-list-item-title>
            </v-list-item>
            <v-list dense min-width="150" class="overflow-y-auto">
              <v-list-item
                v-for="(label, j) in task.labels"
                :key="j"
                :ref="'label-' + label.id"
                @click="$emit('selected', label.id)"
              >
                <v-list-item-content>
                  <span
                    v-shortkey="[letter_dict[label.name]]"
                    @shortkey="$emit('selected', label.id)"
                  ></span>

                  <span :class="{ active: label == active_label }">
                    <v-list-item-title
                      v-text="label.name + ' (' + letter_dict[label.name] + ')'"
                    />
                  </span>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </span>
        </v-list>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: 'EntityMenu',
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    tasks: {
      type: Array,
      required: true,
    },
    x: {
      type: Number,
    },
    y: {
      type: Number,
    },
  },
  data() {
    return {
      cursor_index: 0,
    };
  },
  computed: {
    letter_dict() {
      const alphabet = 'abcdefghijklmnopqrstuvwxyz';
      let idx = 0;
      let d = {};
      this.tasks.forEach(t => {
        t.labels.forEach(l => {
          //d[l.name] = alphabet[idx % (alphabet.length - 1)]
          d[l.name] = alphabet[idx];
          idx++;
        });
      });
      return d;
    },
    label_list() {
      return this.tasks
        .map(t => t.labels)
        .reduce((prev, next) => prev.concat(next), []);
    },
    active_label() {
      return this.label_list[this.cursor_index];
    },
    active_task() {
      let count = 0;
      let active_task = null;
      for (var i = 0; i < this.tasks.length; i++) {
        count += this.tasks[i].labels.length;
        if (this.cursor_index < count) {
          active_task = this.tasks[i];
          break;
        }
      }
      return active_task;
    },
  },
  watch: {
    show() {
      this.cursor_index = 0;
    },
    tasks() {
      this.cursor_index = 0;
    },
  },
  methods: {
    selectLabel(name) {
      alert(name);
    },
    scrollToActive() {
      /*this.$nextTick(
          () => {
            this.$refs['label-'+this.active_label.id][0].$el.scrollIntoView({ behavior: 'smooth' })
          }
      )*/
      this.$nextTick(() => {
        this.$refs['task-' + this.active_task.id][0].$el.scrollIntoView({
          behavior: 'smooth',
          block: 'nearest',
          inline: 'start',
        });

        let container = this.$refs['taskList'].$el;
        // let element = this.$refs['label-379'][0].$el
        let element = this.$refs['label-' + this.active_label.id][0].$el;

        const isVisible = function (ele, container) {
          const eleTop = ele.offsetTop;
          const eleBottom = eleTop + ele.clientHeight;

          const containerTop = container.scrollTop;
          const containerBottom = containerTop + container.clientHeight;

          // The element is fully visible in the container
          return (
            (eleTop >= containerTop && eleBottom <= containerBottom) ||
            // Some part of the element is visible in the container
            (eleTop < containerTop && containerTop < eleBottom) ||
            (eleTop < containerBottom && containerBottom < eleBottom)
          );
        };

        if (!isVisible(element, container)) {
          this.$nextTick(() => {
            //if (this.label_list[0] != this.active_label) {
            this.$refs['label-' + this.active_label.id][0].$el.scrollIntoView({
              behavior: 'smooth',
              block: 'nearest',
              inline: 'start',
            });

            //}
          });
        }
      });
    },
    browseLabels(direction) {
      if (direction == 'up') {
        if (this.cursor_index == 0) {
          this.cursor_index = this.label_list.length - 1;
        } else {
          this.cursor_index--;
        }
      }
      if (direction == 'down') {
        if (this.cursor_index == this.label_list.length - 1) {
          this.cursor_index = 0;
        } else {
          this.cursor_index++;
        }
      }
      this.scrollToActive();
    },
    browseTasks(direction) {
      if (direction == 'left') {
        let current_label = this.label_list[this.cursor_index];
        let current_task_idx = this.tasks.findIndex(t => {
          return t.labels.find(l => l == current_label);
        });
        if (current_task_idx == 0) {
          let last_task = this.tasks[this.tasks.length - 1];
          this.cursor_index = this.label_list.length - last_task.labels.length;
        } else {
          let prev_task = this.tasks[current_task_idx - 1];
          this.cursor_index = this.label_list.findIndex(l => {
            return prev_task.labels.find(tl => tl == l);
          });
        }
      }

      if (direction == 'right') {
        let current_label = this.label_list[this.cursor_index];
        let current_task_idx = this.tasks.findIndex(t => {
          return t.labels.find(l => l == current_label);
        });
        if (current_task_idx == this.tasks.length - 1) {
          this.cursor_index = 0;
        } else {
          let next_task = this.tasks[current_task_idx + 1];
          this.cursor_index = this.label_list.findIndex(l => {
            return next_task.labels.find(tl => tl == l);
          });
        }
      }

      this.scrollToActive();
    },
  },
};
</script>

<style scoped lang="scss">
.v-menu__content {
  width: 400px;

  .list-item {
    padding: 30px 40px;
  }

  > .v-list > .v-list > span > .v-list-item {
    background: #91d1ee !important;
    color: white !important;
  }

  > .v-list > .v-list > span.active > .v-list-item,
  > .v-list > .v-list > span:hover > .v-list-item {
    background: #03a9f4 !important;
    color: white !important;
  }
}

span.active > .v-list-item__title,
span > .v-list-item__title:hover {
  color: #03a9f4 !important;
}
</style>
