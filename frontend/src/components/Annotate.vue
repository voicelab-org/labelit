<template>
  <div>
    <div v-if="moreToAnnotate" class="annotation-form">

        <span v-shortkey="['ctrl', 'alt', 'arrowup']" @shortkey.stop="browseTasks('left')"></span>
        <span v-shortkey="['ctrl', 'alt', 'arrowdown']" @shortkey.stop="browseTasks('right')"></span>

        <span v-shortkey="['ctrl', 'enter',]" @shortkey="submit"></span>
        <div v-if="isUndoButtonShown && !reviewMode">
            <v-btn class="primary" @click="undo">UNDO</v-btn>
        </div>
        <div id="doc-container" v-if="document && batch">
            <Document :document="document" :project="batch.project" @loaded="startTiming"/>
        </div>
        <div v-if="batch.project.do_display_timer_time">
          Time: {{time_display}}
        </div>
        <div id="annotation-forms-t" v-if="annotations">
            <div v-if="tasksLoaded">
                <div v-for="(annotation, i) in annotations" :key="annotation.id" :class="getAnnotationClasses(annotation, i == focus_index)">
                    <component
                      :is="getFormForTask(getTaskForAnnotation(annotation))"
                      :annotation="annotation"
                      :time="time"
                      :task="getTaskForAnnotation(annotation)"
                      :submitting="submitting"
                      @submitted="numTasksSubmitted++"
                      @submiterror="handleSubmitError()"
                      :review-mode="reviewMode"
                      :document="document"
                      :focused="i == focus_index"
                      @focus="focus_index = i"
                    />
                    <div v-if="annotation.qa_invalidation_comment">
                        {{annotation.qa_invalidation_comment}}
                    </div>
                </div>
            </div>
        </div>
        <div id="actions-container" v-if="annotations">
            <v-btn @click="submit()" color="primary">SUBMIT</v-btn>
            <hotkey-guide />
        </div>
        <div id="inactive" v-if="isInactive && !batch.project.do_display_timer_time">
            <v-icon>mdi-pause</v-icon>
        </div>
    </div>
    <div v-else>
        No more to annotate.
    </div>
    <div>
      batch.project.does_audio_playing_count_as_activity: {{batch.project.does_audio_playing_count_as_activity}}
    </div>
  </div>
</template>

<script>
import BatchService from '@/services/batch.service'
import TaskService from '@/services/task.service'
import QA from './mixins/QA.js'
import Timer from './mixins/Timer.js'
import Document from './Document'
import HotkeyGuide from '@/components/HotkeyGuide'

export default {
  name: 'annotate',
  components: {
    Document,
    HotkeyGuide,
  },
  mixins: [
    QA,
    Timer,
  ],
  props: {
    batchId: {
        type: String,
        required: true,
    },
    reviewMode: {
        type: Boolean,
        default: false
    },
  },
  data(){
    return {
        batch: null,
        annotations: null,
        tasks: null,
        document: null,
        submitting: false,
        numTasksSubmitted: 0,
        moreToAnnotate: true,
        isUndoing: false,
        isFirstAnnotation: true,
        focus_index: 0,
    }
  },
  created(){
    this.getBatch()
    this.getNextDocument(true)

    this.$store.commit('entities/ENABLE_ANNOTATION')
  },
  methods: {
    getBatch(){
        BatchService.getBatchById(this.batchId)
            .then((response) => {
                this.batch = response.data
            })
            .catch(function(error){
                console.log(error)
            })
    },
    undo(){
        let vm = this
        vm.isUndoing = true
        vm.annotations = null
        vm.tasks = null
        vm.submitting = false
        vm.numTasksSubmitted = 0
        BatchService.getDocumentToUndo(vm.batchId)
            .then((response) => {
                vm.annotations = response.data.annotations
                vm.document = response.data.document
                vm.getTasks()
            })
    },
    getNextDocument(isFirstAnnotation){
        let vm = this
        this.focus_index = 0
        this.$store.commit('entities/CLEAR_ANNOTATED_ENTITIES')
        vm.annotations = null
        vm.tasks = null
        vm.submitting = false
        vm.numTasksSubmitted = 0
        let getNext = (vm.reviewMode) ? 'getNextDocumentToReview' : 'getBatchNextDocument'
        BatchService[getNext](vm.batchId)
            .then(function(response){
                vm.annotations = response.data.annotations
                vm.document = response.data.document
                vm.getTasks()
            })
            .catch(function(error){
                if (error.response.status == 404){
                    vm.moreToAnnotate = false
                }
            })
        vm.isUndoing = false
        if (!isFirstAnnotation){
            vm.isFirstAnnotation = false
        }
    },
    submit(){
        this.submitting = true
    },
    getTasks(){
        let vm = this
        vm.annotations.forEach(
            function(annotation){
                TaskService.getTaskById(annotation.task)
                    .then(function(response){
                        if (vm.tasks == null) vm.tasks = []
                        vm.tasks.push(response.data)
                    })
                    .catch(err => console.log(err))
            }
        )
    },
    getTaskForAnnotation(annotation){
        var vm = this
        return vm.tasks.filter(t=>t.id == annotation.task)[0]
    },
    getFormForTask(task){
        return task.resourcetype+'Form'
    },
    handleSubmitError(){
        this.submitting = false
        this.numTasksSubmitted = 0
    },
    browseTasks(direction) {

      if (direction == 'right') {
        if (this.focus_index == this.annotations.length - 1) {
          this.focus_index = 0
        } else {
          this.focus_index++
        }
      }

      if (direction == 'left') {
        if (this.focus_index == 0) {
          this.focus_index = this.annotations.length - 1
        } else {
          this.focus_index--
        }
      }

    },
  },
  computed: {
    time_display(){
      return Math.round(this.time / 1000, 2)
    },
    tasksLoaded(){
        var vm = this
        if (vm.annotations == null) return false
        if (vm.tasks == null) return false
        return vm.annotations.length == vm.tasks.length
    },
    allSubmitted(){
       return this.numTasksSubmitted == this.tasks.length
    },
    isUndoButtonShown(){
        return !this.isUndoing && !this.isFirstAnnotation
    },
  },
  watch: {
    numTasksSubmitted(val){
        let vm = this
      if (!this.tasks){
        return
      } else {
        if (val == this.tasks.length && val!==0){
            vm.submitting = false
            vm.getNextDocument()
        }
      }
      /*if (val == this.tasks.length && val!==0){
            vm.submitting = false
            vm.getNextDocument()
        }*/
    },
  },
}
</script>
<style scoped lang="scss">
#actions-container{
    margin-top: 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.annotation-form {
    position: relative;
    padding: 10px 0;
    #inactive {
        display: flex;
        justify-content: space-around;
        align-items: center;

        background: black;
        opacity: 0.8;
        position: fixed;
        top: 0;
        height: 100%;
        z-index: 2000;
        width: calc(100% + 52px);
        left: -50px;
        > .v-icon {
            opacity: 1;
            color: white;
            font-size: 100px;
        }
    }
}

</style>

