<template>
  <span :class="[newline ? 'newline' : '']">
    <span 
        v-if="label"
        :style="{ borderColor: color, cursor: 'pointer' }"
        class="highlight bottom"
        @click="$emit('click', $event)"
    >
      <span class="highlight__content">{{ content }}<v-icon class="delete"
                @click.stop="remove"
                v-show="enabled"
        >mdi-close-circle
        </v-icon>
      </span>
      <span
          :data-label="label.name" :style="{ backgroundColor: color, color: textColor }" class="highlight__label"/>
      </span>
    <span v-else >{{ content }}</span>
  </span>

</template>

<script>

export default {
  props: {
    content: {
      type: String,
      default: '',
      required: true
    },
    label: {
      type: Object,
      default: null,
    },
    color: {
      type: String,
      default: '#64FFDA'
    },
    labels: {
      type: Array,
      default: () => [],
      required: true
    },
    newline: {
      type: Boolean
    },
    enabled: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      showMenu: false
    }
  },
  computed: {
    textColor() {
      return this.idealColor(this.color)
    }
  },
  methods: {
    update(label) {
      this.$emit('update', label)
      this.showMenu = false
    },
    remove() {
      this.$emit('remove')
    },
    idealColor(hexString) {
      // W3c offers a formula for calculating ideal color:
      // https://www.w3.org/TR/AERT/#color-contrast
      const r = parseInt(hexString.substr(1, 2), 16)
      const g = parseInt(hexString.substr(3, 2), 16)
      const b = parseInt(hexString.substr(5, 2), 16)
      return ((((r * 299) + (g * 587) + (b * 114)) / 1000) < 128) ? '#ffffff' : '#000000'
    },
  }
}
</script>

<style scoped>
.highlight.blue {
  background: #edf4fa !important;
}

.highlight.bottom {
  display: block;
  white-space: normal;
}

.highlight:first-child {
  margin-left: 0;
}

.highlight {
  border: 2px solid;
  border-radius: 4px;
  margin: 4px 6px 4px 3px;
  vertical-align: middle;
  position: relative;
  cursor: default;
  min-width: 26px;
  line-height: 22px;
  display: flex;
}

.highlight .delete {
  top: -15px;
  left: -13px;
  position: absolute;
  display: none;
}

.highlight:hover .delete {
  display: block;
}

.highlight__content {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  padding: 2px 2px 0px 6px;
}

.highlight.bottom .highlight__content:after {
  content: " ";
  padding-right: 3px;
}

.highlight__label {
  line-height: 14px;
  padding-top: 1px;
  align-items: center;
  justify-content: center;
  display: flex;
  padding: 0 8px;
  text-align: center;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  color: white;
}

.highlight__label::after {
  content: attr(data-label);
  display: block;
  font-size: 14px;
  -webkit-font-smoothing: subpixel-antialiased;
  letter-spacing: .1em;
}

.newline {
  width: 100%;
}

.break {
  flex-basis: 100%;
  height: 0;
}
</style>
