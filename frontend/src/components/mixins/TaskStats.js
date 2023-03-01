import TaskService from '@/services/task.service.js';

export default {
  name: 'TaskStats',
  mixins: [],
  props: {
    task: {
      type: Object,
      required: true,
    },
    batchId: {
      type: Number,
    },
    projectId: {
      type: Number,
    },
  },
  data() {
    return {
      stats: null,
    };
  },
  created() {
    if (this.batchId) {
      TaskService.getBatchStats(this.task.id, { batch_id: this.batchId }).then(
        res => {
          this.stats = res.data;
        }
      );
    } else {
      TaskService.getProjectStats(this.task.id, {
        project_id: this.projectId,
      }).then(res => {
        this.stats = res.data;
      });
    }
  },
};
