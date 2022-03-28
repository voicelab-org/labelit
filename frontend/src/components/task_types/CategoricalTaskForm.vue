<template>
    <div class="task-form-container">
        <TaskFormHeader
            :task="task"
            :read-only="readOnly"
        />
        <LabelSet :focused="focused" :read-only="readOnly" :labels="task.labels" v-model="selected_labels" :are-labels-exclusive="task.are_categories_exclusive" />
        <ValidationError :message="validationError" />
    </div>
</template>
<script>


import LabelSet from '@/components/LabelSet'
import TaskForm from '@/components/mixins/TaskForm'
import ValidationError from '@/components/ValidationError'
import TaskFormHeader from '@/components/TaskFormHeader'

export default {
    name: 'categorical-task-form',
    components: {
        LabelSet,
        ValidationError,
        TaskFormHeader,
    },
    mixins: [TaskForm],

}
</script>

<style lang="scss">

.task-form-container{
    margin-bottom: 15px;
}

</style>
