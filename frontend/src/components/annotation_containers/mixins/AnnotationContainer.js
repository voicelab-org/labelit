import ProjectTaskService from "@/services/project_task.service";
import Project_taskService from "@/services/project_task.service";

export default {
    name: 'AnnotationContainer',
    props: {
        document: {
            type: Object,
            required: true
        },
        project: {
            type: Object,
            required: true,
        },
        annotations: {
            type: Array,
            required: true,
        },
        tasks: {
            type: Array,
            required: true,
        },
        time: {
            type: Number,
        },
        submitting: {
            type: Boolean,
            required: true,
        },
        reviewMode: {
            type: Boolean,
        },
    },
    created() {
        this.getProjectTasks()

    },
    data() {
        return {
            project_tasks: null,
            sorted_annotations: null,
        }
    },
    methods: {
        getProjectTasks() {
            Project_taskService.list({params: {project: this.project.id}}).then(
                (res) => {
                    this.project_tasks = res.data
                    this.sorted_annotations = JSON.parse(JSON.stringify(this.annotations)).sort(
                        (a, b) => {
                            let a_project_task = this.project_tasks.filter(pt => pt.task == a.task)[0]
                            let b_project_task = this.project_tasks.filter(pt => pt.task == b.task)[0]

                            let a_order = a_project_task.order
                            let b_order = b_project_task.order
                            if (a_order < b_order) {
                                return -1
                            }
                            if (a_order > b_order) {
                                return 1
                            }
                            return 0
                        }
                    )
                }
            )

        },
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
