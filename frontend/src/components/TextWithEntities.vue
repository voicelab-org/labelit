<template>
  <div>
    <div
      class="highlight-container highlight-container--bottom-labels"
      @click="open"
      @touchend="open"
    >
      <entity-item
        v-for="(chunk, i) in chunks"
        :key="i"
        :content="chunk.text"
        :newline="chunk.newline"
        :label="chunk.label"
        :color="getChunkColor(chunk)"
        :labels="labels"
        :enabled="enabled"
        @remove="removeEntity(chunk)"
        @click.stop="openEditEntity(chunk, $event)"
      />
      <EntityMenu
        :show="showMenu"
        :tasks="tasks"
        :x="x"
        :y="y"
        @selected="assignLabel"
      />
    </div>
  </div>
</template>

<script>
// most code from https://github.com/doccano/doccano/blob/master/LICENSE

import EntityItem from '@/components/EntityItem.vue';
import EntityMenu from '@/components/EntityMenu.vue';

export default {
  name: 'TextWithEntities',
  components: {
    EntityItem,
    EntityMenu,
  },
  props: {
    text: {
      type: String,
      //default: '',
      default:
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum',
      required: true,
    },
    tasks: {
      type: Array,
      required: true,
    },
    value: {
      // annotated entities
      type: Array,
      required: true,
    },
    enabled: {
      type: Boolean,
      default: true,
    },
    fullWords: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      showMenu: false,
      x: 0,
      y: 0,
      start: 0,
      end: 0,
      annotated_entities: this.value,
    };
  },
  computed: {
    sortedEntities() {
      return this.annotated_entities
        .slice()
        .sort((a, b) => a.start_offset - b.start_offset);
    },

    chunks() {
      let chunks = [];
      const entities = this.sortedEntities;
      let startOffset = 0;
      for (const entity of entities) {
        const entity_end_with_newline = this.text
          .slice(entity.start_offset, entity.end_offset)
          .includes('\n')
          ? true
          : false;
        // add non-entities to chunks.
        chunks = chunks.concat(
          this.makeChunks(this.text.slice(startOffset, entity.start_offset))
        );
        startOffset = entity_end_with_newline
          ? entity.end_offset - 1
          : entity.end_offset;

        // add entities to chunks.
        entity.end_offset = startOffset;
        const label = this.labels.find(l => l.name == entity.name);
        chunks.push({
          label: label,
          color: label.background_color,
          text: this.text.slice(entity.start_offset, entity.end_offset),
          start_offset: entity.start_offset,
          end_offset: entity.end_offset,
          newline: false,
        });
      }
      // add the rest of text.
      chunks = chunks.concat(
        this.makeChunks(this.text.slice(startOffset, this.text.length))
      );
      return chunks;
    },
    labels() {
      var labels = [];
      this.tasks.forEach(t => {
        t.labels.forEach(l => {
          labels.push(l);
        });
      });
      return labels;
    },
  },
  watch: {
    value() {
      this.annotated_entities = this.value; // HACK
    },
  },
  methods: {
    openEditEntity(chunk, event) {
      this.start = chunk.start_offset;
      this.end = chunk.end_offset;
      this.show(event);
    },
    getChunkColor(chunk) {
      if (!chunk.label) {
        return;
      }
      return chunk.label.color;
    },
    updateEntity(startOffset, endOffset, labelId) {
      // remove old label
      this.annotated_entities = this.annotated_entities.filter(e => {
        return !(e.start_offset == startOffset && e.end_offset == endOffset);
      });
      // add new label
      let label = this.labels.find(l => l.id == labelId);
      let edited_label = Object.assign({}, label);
      delete edited_label.id;
      edited_label.start_offset = startOffset;
      edited_label.end_offset = endOffset;
      this.annotated_entities.push(edited_label);
      this.$emit('input', this.annotated_entities);
    },
    addEntity(startOffset, endOffset, labelId) {
      let label = this.labels.find(l => l.id == labelId);
      let annotated_label = Object.assign({}, label);
      delete annotated_label.id;
      annotated_label.start_offset = startOffset;
      annotated_label.end_offset = endOffset;
      this.annotated_entities.push(annotated_label);
    },
    removeEntity(chunk) {
      this.annotated_entities = this.annotated_entities.filter(e => {
        return !(
          e.start_offset == chunk.start_offset &&
          e.end_offset == chunk.end_offset
        );
      });
      this.$emit('input', this.annotated_entities);
    },
    makeChunks(text) {
      const chunks = [];
      const snippets = text.split('\n');
      for (const snippet of snippets.slice(0, -1)) {
        chunks.push({
          label: null,
          color: null,
          text: snippet + '\n',
          newline: false,
        });
        chunks.push({
          label: null,
          color: null,
          text: '',
          newline: true,
        });
      }
      chunks.push({
        label: null,
        color: null,
        text: snippets.slice(-1)[0],
        newline: false,
      });
      return chunks;
    },
    show(e) {
      e.preventDefault();
      this.showMenu = false;
      if (this.enabled) {
        this.x = e.clientX || e.changedTouches[0].clientX;
        this.y = e.clientY || e.changedTouches[0].clientY;
        this.$nextTick(() => {
          this.showMenu = true;
        });
      }
    },
    setSpanInfo() {
      let selection;
      // Modern browsers.
      if (window.getSelection) {
        selection = window.getSelection();
      } else if (document.selection) {
        selection = document.selection;
      }
      // If nothing is selected.
      if (selection.rangeCount <= 0) {
        return;
      }
      const range = selection.getRangeAt(0);
      const preSelectionRange = range.cloneRange();
      preSelectionRange.selectNodeContents(this.$el);
      preSelectionRange.setEnd(range.startContainer, range.startOffset);
      this.start = [...preSelectionRange.toString()].length;
      this.end = this.start + [...range.toString()].length;
    },
    validateSpan() {
      if (
        typeof this.start === 'undefined' ||
        typeof this.end === 'undefined'
      ) {
        return false;
      }
      if (this.start === this.end) {
        return false;
      }
      for (const entity of this.annotated_entities) {
        if (
          entity.start_offset <= this.start &&
          this.start < entity.end_offset
        ) {
          return false;
        }
        if (entity.start_offset < this.end && this.end <= entity.end_offset) {
          return false;
        }
        if (this.start < entity.start_offset && entity.end_offset < this.end) {
          return false;
        }
      }
      return true;
    },
    adjustSelection() {
      let selection;
      // Modern browsers.
      if (window.getSelection) {
        selection = window.getSelection();
      } else if (document.selection) {
        selection = document.selection;
      }
      // If nothing is selected.
      if (selection.rangeCount <= 0) {
        return;
      }
      const range = selection.getRangeAt(0);
      var rangeStr = range.toString();

      var prefix = '';
      if (
        range.startContainer.nodeName == '#text' &&
        rangeStr[0] != ' ' &&
        range.startOffset != range.startContainer.textContent.length
      ) {
        var txt = range.startContainer.textContent;
        var start = range.startOffset;
        while (start != 0) {
          start--;
          if (txt[start] == ' ') break;
          prefix = txt[start] + prefix;
        }
        //range.setStart(range.startContainer, range.startOffset - prefix.length)
        range.setStart(range.startContainer, range.startOffset - prefix.length);
      } else {
        if (rangeStr[0] == ' ') {
          if (range.endContainer.nodeName == '#text') {
            range.setStart(range.endContainer, range.startOffset + 1);
          } else {
            range.setStart(range.endContainer, range.endOffset);
          }
        }
      }

      var suffix = '';

      if (
        range.endContainer.nodeName == '#text' &&
        rangeStr[rangeStr.length - 1] != ' ' &&
        range.endOffset != 0
      ) {
        txt = range.endContainer.textContent;
        var end = range.endOffset;
        while (end < txt.length) {
          if (txt[end] == ' ') break;
          suffix += txt[end];
          end++;
        }
        range.setEnd(range.endContainer, range.endOffset + suffix.length);
      } else {
        if (rangeStr[rangeStr.length - 1] == ' ') {
          range.setEnd(range.endContainer, range.endOffset - 1);
        }
      }
    },
    open(e) {
      if (this.fullWords) {
        this.adjustSelection();
      }
      this.setSpanInfo();
      if (this.validateSpan()) {
        this.show(e);
      }
    },
    assignLabel(labelId) {
      if (
        this.annotated_entities.find(
          e => e.start_offset == this.start && e.end_offset == this.end
        )
      ) {
        this.updateEntity(this.start, this.end, labelId);
      } else {
        if (this.validateSpan()) {
          this.addEntity(this.start, this.end, labelId);
        }
      }

      this.showMenu = false;
      this.start = 0;
      this.end = 0;
    },
  },
};
</script>

<style scoped>
.highlight-container.highlight-container--bottom-labels {
  align-items: flex-start;
}

.highlight-container {
  line-height: 42px !important;
  white-space: pre-wrap;
  cursor: default;
  display: flex;
  flex-wrap: wrap;
}

.highlight-container.highlight-container--bottom-labels .highlight.bottom {
  margin-top: 6px;
}
</style>
