<template>
  <div>
    <div
      v-if="((numberOfAnnotations && batch) || project) && stats"
      class="general-stats"
    >
      <h4>{{ $t('Global statistics') }}</h4>
      <table class="stats-table">
        <tr>
          <td class="left">{{ $t('Total number of annotations') }}</td>
          <td>{{ stats.num_annotations }}</td>
        </tr>
        <template v-if="batch">
          <tr>
            <td class="left">
              {{ $t('Progress (documents fully annotated / total documents)') }}
            </td>
            <td>{{ stats.num_done }} / {{ batch.num_documents }}</td>
          </tr>
          <tr>
            <td class="left">{{ $t('Dataset') }}</td>
            <td>{{ batch.dataset.name }}</td>
          </tr>
          <tr>
            <td class="left">{{ $t('Number of annotators') }}</td>
            <td>{{ batch.annotators.length }}</td>
          </tr>
          <tr>
            <td class="left">{{ $t('Number of annotators per document') }}</td>
            <td>{{ batch.num_annotators_per_document }}</td>
          </tr>
          <tr>
            <td class="left">{{ $t('Document distribution mode') }}</td>
            <td>{{ batch.annotation_mode }}</td>
          </tr>
        </template>
        <template v-if="project">
          <tr>
            <td class="left">
              {{ $t('Number of documents fully annotated') }}
            </td>
            <td>{{ stats.num_done }}</td>
          </tr>
        </template>
        <tr>
          <td class="left">
            {{ $t('Average annotation time per annotated document') }}
          </td>
          <td>
            <span v-if="stats.num_done">{{ average_time }} s</span
            ><span v-else>N/A</span>
          </td>
        </tr>
        <tr v-if="proj.is_audio_annotated">
          <td class="left">{{ $t('Average audio time') }}</td>
          <td>
            <span v-if="stats.num_done"
              >{{ toSeconds(stats.average_duration.average) }} s</span
            ><span v-else>N/A</span>
          </td>
        </tr>
        <tr v-if="proj.is_audio_annotated">
          <td class="left">{{ $t('Average annotation/audio time ratio') }}</td>
          <td>
            <span v-if="stats.num_done">{{ rounded_ratio }}</span
            ><span v-else>N/A</span>
          </td>
        </tr>
        <tr>
          <td class="left">
            {{ $t('Number of annotations pending review') }}
          </td>
          <td>{{ stats.num_to_review }}</td>
        </tr>
        <tr>
          <td class="left">
            {{ $t('Number of annotations reviewed by QA') }}
          </td>
          <td>{{ stats.num_qa_seen }}</td>
        </tr>
        <tr>
          <td class="left">
            {{ $t('Number of annotations validated by QA') }}
          </td>
          <td>{{ stats.num_validated }}</td>
        </tr>
        <tr>
          <td class="left">
            {{ $t('Number of annotations invalidated by QA') }}
          </td>
          <td>{{ stats.num_invalidated }}</td>
        </tr>
      </table>
      <h4>{{ $t('Annotator statistics') }}</h4>
      <table class="stats-table">
        <tr>
          <th></th>
          <th>{{ $t('Number of documents annotated') }}</th>
          <th v-if="proj.is_audio_annotated">
            {{ $t('Average annotation/audio time ratio') }}
          </th>
        </tr>
        <tr v-for="a_stats in stats.annotator_stats" :key="a_stats.name">
          <td>
            {{ a_stats.name }}
          </td>
          <td>
            {{ a_stats.num_documents_annotated }}
          </td>

          <td v-if="proj.is_audio_annotated">
            {{ a_stats.average_ratio.average }}
          </td>
        </tr>
      </table>

      <template v-if="batch">
        <div v-for="task in proj.tasks" :key="task.id">
          <template v-if="statsComponentExist(task)">
            <component
              :is="getTaskStatsComponent(task)"
              :task="task"
              :batch-id="batch.id"
            />
          </template>
        </div>
      </template>
      <template v-if="project">
        <div v-for="task in proj.tasks" :key="task.id">
          <template v-if="statsComponentExist(task)">
            <component
              :is="getTaskStatsComponent(task)"
              :task="task"
              :project-id="project.id"
            />
          </template>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import BatchService from '@/services/batch.service.js';
import ProjectService from '@/services/project.service.js';

export default {
  name: 'Stats',
  props: {
    batchId: {
      type: String,
    },
    projectId: {
      type: Number,
    },
  },
  data() {
    return {
      numberOfAnnotations: [],
      batch: null,
      project: null,
      stats: null,
    };
  },
  computed: {
    average_time() {
      if (this.stats) {
        return parseInt(this.stats.average_time_per_document.average / 1000);
      }
      return null;
    },
    rounded_ratio() {
      return Math.round(this.stats.average_ratio.average * 10) / 10;
    },
    proj() {
      if (this.batch) return this.batch.project;
      if (this.project) return this.project;
      return null;
    },
  },
  created() {
    let vm = this;

    if (this.batchId) {
      vm.getNumberOfAnnotations();
      vm.getBatch();
    }
    if (this.projectId) {
      vm.getProject();
    }
    vm.getStats();
  },
  methods: {
    statsComponentExist(task) {
      return Object.keys(this.$options.components).includes(
        this.getTaskStatsComponent(task)
      );
    },
    getTaskStatsComponent(task) {
      return task.resourcetype + 'Stats';
    },
    getNumberOfAnnotations() {
      var vm = this;
      BatchService.getNumberOfAnnotationsForUser(vm.batchId)
        .then(function (res) {
          vm.numberOfAnnotations = res.data;
        })
        .catch(err => {
          console.error(err);
        });
    },
    getBatch() {
      BatchService.getBatchById(this.batchId).then(res => {
        this.batch = res.data;
      });
    },
    getProject() {
      ProjectService.getProjectById(this.projectId).then(res => {
        this.project = res.data;
      });
    },
    getStats() {
      if (this.batchId) {
        BatchService.getStats(this.batchId).then(res => {
          this.stats = res.data;
        });
      }

      if (this.projectId) {
        ProjectService.getStats(this.projectId).then(res => {
          this.stats = res.data;
        });
      }
    },
    toSeconds(ms) {
      return parseInt((ms / 1000) * 100) / 100;
    },
  },
};
</script>
<style scoped lang="scss">
.task-stats {
  margin-top: 20px;
}

.general-stats > table {
  margin-bottom: 25px;
}
</style>
