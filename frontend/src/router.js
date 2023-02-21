import Vue from "vue";
import VueRouter from "vue-router";
import store from "@/store/index";
import Annotate from "./components/Annotate";
import Stats from "./components/Stats";
import QA from "./components/QA";
import Review from "./components/Review";
import Batch from "./components/Batch";

Vue.use(VueRouter);

let router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/login",
      name: "login",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "Login" */ "./views/Login.vue"),
    },
    {
      path: "/lexicons",
      name: "lexicons",
      component: () =>
        import(
          /* webpackChunkName: "DatasetList" */ "./components/LexiconList.vue"
        ),
    },

    {
      path: "/lexicon/:id",
      component: () =>
        import(/* webpackChunkName: "Task" */ "./components/Lexicon.vue"),
      props: (route) => ({ id: route.params.id }),
    },
    {
      path: "/dashboard",
      name: "dashboard",
      redirect: "/dashboard/stats/",
      component: () =>
        import(
          /* webpackChunkName: "DatasetList" */ "./components/Dashboard.vue"
        ),
      children: [
        {
          path: "/dashboard/projects",
          name: "dashboard-projects",
          component: () =>
            import(
              /* webpackChunkName: "DatasetList" */ "./components/DashboardProjects.vue"
            ),
        },
        {
          path: "/dashboard/stats",
          name: "dashboard-stats",
          component: () =>
            import(
              /* webpackChunkName: "DatasetList" */ "./components/DashboardStats.vue"
            ),
        },
      ],
    },

    {
      path: "/projects",
      name: "projects",
      component: () =>
        import(
          /* webpackChunkName: "DatasetList" */ "./components/ProjectList.vue"
        ),
    },
    {
      path: "/tasks",
      name: "tasks",
      component: () =>
        import(
          /* webpackChunkName: "DatasetList" */ "./components/TaskList.vue"
        ),
    },
    {
      path: "/task/:id",
      component: () =>
        import(/* webpackChunkName: "Task" */ "./components/Task.vue"),
      props: (route) => ({ taskId: route.params.id }),
    },
    {
      path: "/datasets",
      component: () =>
        import(
          /* webpackChunkName: "DatasetList" */ "./components/DatasetList.vue"
        ),
    },
    {
      path: "/project/:id",
      component: () =>
        import(/* webpackChunkName: "Project" */ "./components/Project.vue"),
      props: (route) => ({ projectId: route.params.id }),
    },
    {
      path: "/batch/:id",
      component: () =>
        import(/* webpackChunkName: "Batch" */ "./components/Batch.vue"),
      props: (route) => ({ batchId: route.params.id }),
      children: [
        {
          path: "",
          component: Batch,
          beforeEnter: (to, from, next) => {
            const user = store.getters["auth/user"];
            if (user.is_staff) {
              next(`/batch/${to.params.id}/qa`);
            } else {
              next(`/batch/${to.params.id}/annotate`);
            }
          },
          props: (route) => ({ batchId: route.params.id }),
        },
        {
          path: "annotate",
          component: Annotate,
          props: (route) => ({ batchId: route.params.id }),
        },
        {
          path: "stats",
          component: Stats,
          props: (route) => ({ batchId: route.params.id }),
        },
        {
          path: "qa",
          component: QA,
          props: (route) => ({ batchId: route.params.id }),
        },

        {
          path: "review",
          component: Review,
          props: (route) => ({ batchId: route.params.id }),
        },
      ],
    },
    //  { path: '*', redirect: '/projects' }
  ],
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ["/login"];
  const authRequired = !publicPages.includes(to.path);
  const isAuthenticated = store.getters["auth/isAuthenticated"];

  if (authRequired && !isAuthenticated) {
    return next("/login");
  }

  if (isAuthenticated && to.name === "login") {
    return next("projects");
  }

  return next();
});

export default router;
