<template>
  <div>
    <div v-if="batch">
      <div class="header">
        <h2>Batch: {{ batch.name }}</h2>
        <h4 v-if="total_units">
          Progress (batch-level): {{ num_done_units }} / {{ total_units }}
        </h4>
      </div>
      <v-tabs>
        <v-tab v-for="link in links" :key="link.dest" :to="link.dest">
          {{ link.name }}
          <span v-if="link.name == 'Review'">
            <v-badge
              v-if="to_review_count !== null"
              right
              inline
              color="orange"
              :content="to_review_count.toString()"
              value="true"
            >
            </v-badge>
          </span>
        </v-tab>
      </v-tabs>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import BatchService from "@/services/batch.service";
import ProjectService from "@/services/project.service";
import { mapGetters } from "vuex";

export default {
  name: "batch",
  props: {
    batchId: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapGetters({
      user: "auth/user",
    }),
    basePath() {
      return "/batch/" + this.batchId + "/";
    },
    links() {
      var vm = this;
      if (this.user.is_staff) {
        var links = [
          {
            name: "QA",
            dest: vm.basePath + "qa",
          },
        ];
      } else {
        links = [
          {
            name: "Annotate",
            dest: vm.basePath + "annotate",
          },
          {
            name: "Review",
            dest: vm.basePath + "review",
          },
        ];
      }

      links = links.concat([
        {
          name: "Stats",
          dest: vm.basePath + "stats",
        },
      ]);
      return links;
    },
  },
  data() {
    return {
      batch: null,
      total_units: null,
      num_done_units: null,
      to_review_count: null,
    };
  },
  created() {
    let vm = this;
    BatchService.getBatchById(vm.batchId)
      .then(function (response) {
        vm.batch = response.data;
        ProjectService.getProjectById(response.data.project.id)
          .then(function (res) {
            vm.$store.commit("task/SET_TASK_LIST", res.data.tasks);
          })
          .catch((error) => console.log(error));
      })
      .catch((error) => console.log(error));
    this.getProgress();
    BatchService.getNumToReview(vm.batchId).then(function (response) {
      vm.to_review_count = response.data.count;
    });
  },
  methods: {
    getProgress() {
      var vm = this;
      BatchService.getBatchByIdProgress(vm.batchId)
        .then((res) => {
          vm.total_units = res.data.total;
          vm.num_done_units = res.data.num_done_units;
        })
        .catch((err) => console.log(err));
      return;
    },
  },
};
</script>
