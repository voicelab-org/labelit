<template>
  <div>
    <div v-if="focused">

      <span v-shortkey="['arrowleft']" @shortkey="browseLabels('left')"></span>
      <span v-shortkey="['arrowright']" @shortkey="browseLabels('right')"></span>
      <span v-shortkey="['enter']" @shortkey="toggleLabel(orderedLabels[cursor_index])"></span>
    </div>
    <div>
    </div>
    <div class="button-list">
      <v-btn class="label" v-for="(label, i) in orderedLabels" :key="label.name"
             @click="toggleLabel(label)" :class="getLabelClasses(label, i)"
             :depressed="isLabelSelected(label) "
             :color="getLabelColor(label)"
             :disabled="readOnly"
      >
        <span class="label-pill" :style="getLabelPillStyle(label)"></span>
        {{ label[valueField] }}
      </v-btn>
    </div>
  </div>
</template>
<script>
export default {
  name: "label-set",
  props: {
    labels: {
      type: Array,
      required: true,
    },
    value: {  // selected labels
      type: Array,
      required: true,
    },
    areLabelsExclusive: {
      type: Boolean,
      default: true,
    },
    valueField: {
      type: String,
      default: 'name'
    },
    orderBy: {
      type: String,
      default: 'name',
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
    focused: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      cursor_index: 0,
    }
  },
  methods: {
    getLabelPillStyle(label) {
      return {
        'background-color': label.color,
      }
    },
    isLabelSelected(label) {
      return this.value.filter(l => l[this.valueField] == label[this.valueField]).length > 0
    },
    getLabelClasses(label, i) {
      var classes = {
        'selected': false,
        'focused': i == this.cursor_index && this.focused,
      }
      if (this.isLabelSelected(label)) {
        classes['selected'] = true
      }
      return classes
    },
    toggleLabel(label) {

      var newLabels = []
      Object.assign(newLabels, this.value);

      if (newLabels.find(l => l.name == label.name)) {
        newLabels = newLabels.filter(l => l.name != label.name)
      } else {
        if (this.areLabelsExclusive) {
          newLabels = []
        }
        newLabels.push(label)
      }
      this.$emit('input', newLabels)
    },
    getLabelColor(label) {
      if (this.isLabelSelected(label)) {
        return "primary"
      }
    },
    browseLabels(direction) {
      if (direction == 'right') {
        if (this.cursor_index == this.orderedLabels.length - 1) {
          this.cursor_index = 0
        } else {
          this.cursor_index++
        }
      }

      if (direction == 'left') {
        if (this.cursor_index == 0) {
          this.cursor_index = this.orderedLabels.length - 1
        } else {
          this.cursor_index--
        }
      }
    }
  },
  computed: {
    orderedLabels() {
      var vm = this

      var labelsCopy = []
      Object.assign(labelsCopy, vm.labels)
      return labelsCopy.sort((a, b) => {
        return a[vm.valueField] > b[vm.valueField] ? 1 : -1
      })
    },
  },
}
</script>
<style>

.v-btn.label {
  margin-top: 15px;
  margin-right: 25px;
}

.v-btn.label.focused{
  border: 2px solid #03a9f4 !important;
}

.v-btn.label.selected.primary.focused {

  border: 2px solid #006494 !important;
}

</style>