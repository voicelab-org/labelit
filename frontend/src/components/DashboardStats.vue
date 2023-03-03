<template>
  <div>
    <div v-if="projects && annotators">
      <div>
        <div id="stats-filters">
          <div>
            <h5>Min date</h5>
            <div class="date">
              <Datepicker v-model="min_date"></Datepicker>
            </div>
          </div>

          <div>
            <h5>Max date</h5>
            <div class="date">
              <Datepicker v-model="max_date"></Datepicker>
            </div>
          </div>

          <div>
            <h5 id="projs">Projects</h5>
            <v-select
              v-model="filters.projects"
              :items="projects"
              item-text="name"
              item-value="id"
              solo
              flat
              hide-details
              :multiple="true"
            />
          </div>

          <div>
            <h5>Annotators</h5>
            <v-select
              v-model="filters.annotators"
              :items="annotators"
              :item-text="getAnnotatorName"
              item-value="id"
              solo
              flat
              hide-details
              :multiple="true"
            />
          </div>

          <v-btn color="primary" @click="load">
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
        </div>
      </div>
      <br /><br /><br />
      <div v-if="stats && !loading">
        <b> Number of documents annotated: {{ stats.num_docs }} </b>
        <br />
        <b>
          Total duration of annotated audio:
          {{ toHours(stats.total_duration) }} hrs
        </b>
        <br />
        <div class="table-header">
          <h3>Per annotator</h3>
          <ExcelExport
            :data="stats.stats_per_annotator"
            :name="'per-annotator-stats'"
          />
        </div>

        <v-data-table
          :headers="per_annotator_headers"
          :items="stats.stats_per_annotator"
          :items-per-page="15"
          class="elevation-1"
        ></v-data-table>
        <br />

        <div class="table-header">
          <h3>Per annotator and per day</h3>
          <ExcelExport
            :data="stats.stats_per_annotator_per_day"
            :name="'per-annot-per-day-stats'"
          />
        </div>
        <v-data-table
          :headers="per_annotator_and_per_day_headers"
          :items="stats.stats_per_annotator_per_day"
          :sort-by="'day_formatted'"
          :items-per-page="15"
          class="elevation-1"
        ></v-data-table>
      </div>

      <div v-if="loading" class="loading">
        <v-progress-circular
          color="blue-grey"
          indeterminate
        ></v-progress-circular>
      </div>
    </div>
  </div>
</template>
<script>
import DashboardService from '@/services/dashboard.service.js';
import ProjectService from '@/services/project.service.js';
import UserService from '@/services/user.service.js';
import Datepicker from '@/components/Datepicker.vue';
import ExcelExport from '@/components/ExcelExport.vue';

export default {
  name: 'DashboardStats',
  components: {
    Datepicker,
    ExcelExport,
  },
  data() {
    return {
      loading: true,
      stats: null,
      filters: {},
      projects: null,
      annotators: null,
      min_date: null,
      max_date: null,
      per_day_options: {
        sortBy: 'day_formatted',
      },
      per_annotator_and_per_day_headers: [
        {
          text: 'Day',
          align: 'start',
          value: 'day_formatted',
        },
        {
          text: 'Annotator',
          align: 'start',
          value: 'annotator__first_name',
        },
        {
          text: '# docs',
          align: 'start',
          value: 'num_docs',
        },
        {
          text: 'audio duration (hrs)',
          align: 'start',
          value: 'duration_hours',
        },
        {
          text: 'time spent (hrs)',
          align: 'start',
          value: 'annotation_time_hours',
        },
      ],
      per_annotator_headers: [
        {
          text: 'Annotator',
          align: 'start',
          value: 'annotator__first_name',
        },
        {
          text: '# docs',
          align: 'start',
          value: 'num_docs',
        },
        {
          text: 'audio duration (hrs)',
          align: 'start',
          value: 'duration_hours',
        },
        {
          text: 'time spent (hrs)',
          align: 'start',
          value: 'annotation_time_hours',
        },
      ],
    };
  },
  created() {
    UserService.getUserList().then(res => {
      this.annotators = res.data;
    });
    ProjectService.getProjectList().then(res => (this.projects = res.data));
    var max_date = new Date();
    var min_date = new Date();
    min_date.setDate(min_date.getDate() - 2);
    this.min_date = min_date.toISOString().split('T')[0];
    this.max_date = max_date.toISOString().split('T')[0];
    this.load();
  },
  methods: {
    toHours(msDuration) {
      return Number.parseFloat(msDuration / (1000 * 3600)).toPrecision(2);
    },
    load() {
      this.loading = true;

      var params = {
        min_date: this.min_date,
        max_date: this.max_date,
      };
      if (this.filters.projects) {
        params.projects = this.filters.projects.toString();
      }
      if (this.filters.annotators) {
        params.annotators = this.filters.annotators.toString();
      }
      DashboardService.getStats(params).then(res => {
        this.stats = res.data;
        this.stats.stats_per_annotator.forEach(datum => {
          datum.duration_hours = this.toHours(datum.total_duration);
          datum.annotation_time_hours = this.toHours(datum.time_spent);
        });
        this.stats.stats_per_annotator_per_day.forEach(datum => {
          datum.day_formatted = datum.day.split('T')[0];
          datum.duration_hours = this.toHours(datum.total_duration);
          datum.annotation_time_hours = this.toHours(datum.time_spent);
        });
        this.loading = false;
      });
    },
    getAnnotatorName(user) {
      return user.first_name;
    },
  },
};
</script>

<style lang="scss">
.date input {
  border: 1px solid lightgrey;
  border-radius: 3px;
}

#stats-filters {
  display: flex;
  justify-content: space-between;
  align-items: end;

  > div {
    width: 200px;
  }

  .v-input__control {
    border: 1px solid lightgrey;
    border-radius: 3px;
  }
}

.loading {
  margin: 10px 0;
  display: flex;
  justify-content: center;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
