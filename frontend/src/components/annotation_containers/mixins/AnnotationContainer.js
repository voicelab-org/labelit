export default {
    name: 'AnnotationContainer',
    props: {
        document: {
            type: Object,
            required: true
        },
    },
    data() {
        return {}
    },
    methods: {
        getFormForTask(task) {
            return task.resourcetype + 'Form';
        },
        getTaskForAnnotation(annotation) {
            var vm = this;
            return vm.tasks.filter(t => t.id == annotation.task)[0];
        },
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

};
