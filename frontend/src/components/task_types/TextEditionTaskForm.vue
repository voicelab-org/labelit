<template>
  <div class="task-form-container">
    <TaskFormHeader :task="task" :read-only="readOnly" />
    <div v-if="label">
      <textarea
        v-show="label"
        :ref="'edited'"
        v-model="label.edited_text"
        class="transcript"
      />
    </div>
    <ValidationError :message="validationError" />
  </div>
</template>
<script>
import Vue from 'vue';
import TaskForm from '@/components/mixins/TaskForm.vue';
import LabelService from '@/services/label.service.js';
import LexiconService from '@/services/lexicon.service.js';
import ValidationError from '@/components/ValidationError.vue';
import TaskFormHeader from '@/components/TaskFormHeader.vue';

const { Textcomplete } = require('@textcomplete/core');
const { TextareaEditor } = require('@textcomplete/textarea');

export default {
  name: 'TextEditionTaskForm',
  components: {
    ValidationError,
    TaskFormHeader,
  },
  mixins: [TaskForm],
  data() {
    return {
      label: null,
      lexicon: null,
    };
  },
  watch: {
    label: {
      deep: true,
      handler() {
        LabelService.update(this.label.id, this.label).then(() => {
          Vue.set(this.selected_labels, 0, this.label);
        });
        this.$nextTick(() => {
          this.setFocus();
        });
      },
    },
    focused() {
      this.setFocus();
    },
  },
  created() {
    '';
    if (!this.selected_labels.length) {
      var promise = LabelService.create({
        resourcetype: 'TextEditionLabel',
        edited_text: this.document.text,
        task: this.task.id,
      }).then(res => {
        this.label = res.data;
      });
    } else {
      promise = LabelService.get(this.selected_labels[0].id).then(res => {
        this.label = res.data;
      });
    }

    Promise.all([promise]).then(() => {
      LexiconService.getList({
        tasks: this.task.id,
      }).then(res => {
        //this.lexicons = res.data
        this.lexicon = [];

        res.data.forEach(l => {
          this.lexicon = this.lexicon.concat(l.entries.map(e => e.entry));
        });

        //this.$refs.input

        console.log('this.$refs.edited', this.$refs.edited);

        const editor = new TextareaEditor(this.$refs.edited);

        //const textcomplete =
        new Textcomplete(editor, [
          {
            match: /(\S{3,}|\(\w*)$/,
            search: (term, callback) => {
              callback(this.lexicon.filter(l => l.startsWith(term)));
            },
            index: 1,
            replace: function (element) {
              return element + ' ';
            },
          },
        ]);
      });
    });
  },
  mounted() {
    this.setFocus();
  },
  methods: {
    setFocus() {
      if (this.focused) {
        if (this.$refs.edited) {
          this.$refs.edited.focus();
        }
      } else {
        if (this.$refs.edited) {
          this.$refs.edited.blur();
        }
      }
    },
  },
};
</script>

<style lang="scss">
.task-form-container {
  margin-bottom: 15px;

  textarea {
    border: 1px solid lightgrey;
    border-radius: 4px;
    width: 100%;
    min-height: 200px;
  }
}

.textcomplete-dropdown {
  border: 1px solid #ddd;
  background-color: white;
  list-style: none;
  padding: 10;
  margin: 0;
}

.textcomplete-dropdown li {
  margin: 0;
}

.textcomplete-footer,
.textcomplete-item {
  border-top: 1px solid #ddd;
}

.textcomplete-item {
  padding: 2px 5px;
  cursor: pointer;
}

.textcomplete-item:hover,
.textcomplete-item.active {
  background-color: rgb(110, 183, 219);
}

.task-header {
  margin-bottom: 10px;
}

textarea.transcript {
  padding: 10px;
}
</style>
