export default {
  name: 'QA',
  mixins: [],
  methods: {
    getAnnotationClasses(a, is_focused) {
      return {
        annotation: true,
        validated: a.has_qa_validated,
        invalidated: a.has_qa_invalidated,
        resubmitted: a.is_resubmitted,
        is_focused: is_focused,
      };
    },
  },
  created() {
    /*
        send disable entities signal
        */
    this.$store.commit('entities/DISABLE_ANNOTATION');
  },
};
