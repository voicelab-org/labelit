<template>
  <div>
    <div v-if="focused">
      <!--
      <span v-shortkey="['arrowleft']" @shortkey="browseLabels('left')"></span>
      <span v-shortkey="['arrowright']" @shortkey="browseLabels('right')"></span>
      <span v-shortkey="['enter']" @shortkey="toggleLabel(orderedLabels[cursor_index])"></span>
      -->
    </div>
    <div>
      parentlabels: {{ parentLabels }}<br><br>
      label_selections: {{ label_selections }}
    </div>
    <div class="dropdown-list" v-if="label_selections">
      <span v-for="(label, i) in parentLabels" :key="label.label.id">
        <v-select
            :items="label.children"
            v-model="label_selections[i].selections"
            item-text="name"
            item-value="id"
            solo
            flat
            append-icon=keyboard_arrow_down
            hide-details
            :multiple="label.label.single_child_select"
        />
      </span>
    </div>
  </div>
</template>
<script>
export default {
  name: "nested-label-set",
  props: {
    labels: {
      type: Array,
      required: true,
    },
    value: {  // selected labels
      type: Array,
      required: true,
    },
    singleSelect: {
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
      label_selections: null,
    }
  },
  created() {
    this.setSelections()
  },
  watch: {
    label_selections: {
      deep: true,
      handler() {

        if (this.label_selections == null) return

        console.log("label_selections changed", JSON.parse(JSON.stringify(this.label_selections)))
        let selections = this.label_selections.reduce(
            (prev, curr) => {
              console.log("&prev, &curr", JSON.parse(JSON.stringify(prev)), JSON.parse(JSON.stringify(curr)))
              if (!prev.selections) return curr.selections
              return prev.selections.concat(curr.selections)
            },
            []
        )

        console.log("&sel", JSON.parse(JSON.stringify(selections)))

        selections = this.labels.filter(
            (l) => {
              return selections.includes(l.id)
            }
        )

        console.log("&selections", selections)

        this.$emit('input', selections)
      }
    },
  },
  methods: {
    setSelections() {
      let selected_labels = this.value
      this.parentLabels.forEach(
          p_label => {
            let l =
                {
                  parent_label: p_label,
                  selections: selected_labels.filter(l => l.parent_label == p_label.label.id),
                }

            if (!this.label_selections){
              this.label_selections=[l]
              return
            }

            this.label_selections.push(l)
          }
      )
      console.log("&done setSelections, label_sels", this.label_selections)
    },
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
    parentLabels() {
      let parent_labels = this.labels.filter(
          l => l.parent_label == null
      )
      let grouped = []
      parent_labels.forEach(
          (p_label) => {
            grouped.push({
              label: p_label,
              children: this.labels.filter(
                  l => l.parent_label == p_label.id
              ),
            })
          }
      )
      return grouped
    },
  },
}
</script>
<style>

.v-btn.label {
  margin-top: 15px;
  margin-right: 25px;
}

.v-btn.label.focused {
  border: 2px solid #03a9f4 !important;
}

.v-btn.label.selected.primary.focused {

  border: 2px solid #006494 !important;
}

</style>