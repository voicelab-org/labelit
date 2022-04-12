<template>
  <div>
    <div v-if="focused">
      <span v-shortkey="['arrowleft']" @shortkey="browseLabels('left')"></span>
      <span v-shortkey="['arrowright']" @shortkey="browseLabels('right')"></span>
    </div>

    <div class="dropdown-list" v-if="label_selections">
      <div
          :class="getParentLabelClasses(label, i)"
          v-for="(label, i) in parentLabels"
          :key="label.label.id"
      >
        <div class="select">
          <div class="bolder">{{ label.label.name }}</div>
          <v-select
              :items="label.children"
              v-model="label_selections[i].selections"
              item-text="name"
              item-value="id"
              solo
              flat
              hide-details
              :multiple="label.label.single_child_select"
              :ref="'dropdown-'+label.label.id"
              :placeholder="label.label.name"
              autofocus
              :disabled="readOnly"
          />
        </div>
      </div>

        <div v-if="i % 1 == 0" class="break"></div>
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
        let selections = this.label_selections.reduce(
            (prev, curr) => {
              return prev.concat(curr.selections)
            },
            []
        )

        selections = this.labels.filter(
            (l) => {
              return selections.includes(l.id)
            }
        )

        this.$emit('input', selections)
      }
    },
    cursor_index() {
      if (this.focused) {
        this.setDropdownFocus()
      }
    },
    focused() {
      this.setDropdownFocus()
    },
  },
  methods: {
    setDropdownFocus() {
      for (const [index, label] of this.parentLabels.entries()) {
        let ref = 'dropdown-' + label.label.id
        if (index == this.cursor_index) {
          this.$nextTick(() => {

            this.$refs[ref][0].focus()
          })
        } else {
          this.$nextTick(() => {

            this.$refs[ref][0].blur()
          })
        }
      }
    },
    setSelections() {
      let selected_labels = this.value
      this.parentLabels.forEach(
          p_label => {
            let l =
                {
                  parent_label: p_label,
                  selections: selected_labels.filter(l => l.parent_label == p_label.label.id).map(l => l.id),
                }

            if (!this.label_selections) {
              this.label_selections = [l]
              return
            }

            this.label_selections.push(l)
          }
      )
    },
    getLabelPillStyle(label) {
      return {
        'background-color': label.color,
      }
    },
    isLabelSelected(label) {
      return this.value.filter(l => l[this.valueField] == label[this.valueField]).length > 0
    },
    isParentLabelSelected(label) {
      return this.value.filter(l => l.parent_label == label.label.id).length > 0
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
    getParentLabelClasses(label, i) {
      var classes = {
        'focused': i == this.cursor_index && this.focused,
      }
      if (this.isParentLabelSelected(label)) {
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
        if (this.cursor_index == this.parentLabels.length - 1) {
          this.cursor_index = 0
        } else {
          this.cursor_index++
        }
      }

      if (direction == 'left') {
        if (this.cursor_index == 0) {
          this.cursor_index = this.parentLabels.length - 1
        } else {
          this.cursor_index--
        }
      }
    }
  },
  computed: {
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
<style lang="scss">

.dropdown-list  {
  display: flex;
  flex-wrap: wrap;

    > div {
      flex: 0 0 21%; /* explanation below */
      margin: 5px;
      height: 100px;
    }

  div.select {
    display: inline-block;
    max-width: 200px;

    margin-top: 15px;
    margin-right: 25px;

    &.focused {
      /*TODO add focused style*/
      .v-input__control {
        border: 2px solid #03a9f4 !important;
      }

      &.selected {
        .v-input__control {
          border: 2px solid #006494 !important;
        }
      }
    }
  }

  .v-input__control {
    border: 1px solid grey !important;
    border-radius: 4px;
  }

}

</style>