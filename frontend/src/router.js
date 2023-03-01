import Vue from 'vue';
import VueRouter from 'vue-router';
import store from '@/store/index';
import Annotate from '@/components/Annotate.vue';
import Stats from '@/components/Stats.vue';
import QA from '@/components/QA.vue';
import Review from '@/components/Review.vue';
import Batch from '@/components/Batch.vue';

Vue.use(VueRouter);

let router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('@/views/Login.vue'),
    },
    {
      path: '/lexicons',
      name: 'lexicons',
      component: () => import('@/components/LexiconList.vue'),
    },

    {
      path: '/lexicon/:id',
      component: () => import('@/components/Lexicon.vue'),
      props: route => ({ id: route.params.id }),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      redirect: '/dashboard/stats/',
      component: () => import('@/components/Dashboard.vue'),
      children: [
        {
          path: '/dashboard/projects',
          name: 'dashboard-projects',
          component: () => import('@/components/DashboardProjects.vue'),
        },
        {
          path: '/dashboard/stats',
          name: 'dashboard-stats',
          component: () => import('@/components/DashboardStats.vue'),
        },
      ],
    },

    {
      path: '/projects',
      name: 'projects',
      component: () => import('@/components/ProjectList.vue'),
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: () => import('@/components/TaskList.vue'),
    },
    {
      path: '/task/:id',
      component: () => import('@/components/Task.vue'),
      props: route => ({ taskId: route.params.id }),
    },
    {
      path: '/datasets',
      component: () => import('@/components/DatasetList.vue'),
    },
    {
      path: '/project/:id',
      component: () => import('@/components/Project.vue'),
      props: route => ({ projectId: route.params.id }),
    },
    {
      path: '/batch/:id',
      component: () => import('@/components/Batch.vue'),
      props: route => ({ batchId: route.params.id }),
      children: [
        {
          path: '',
          component: Batch,
          beforeEnter: (to, from, next) => {
            const user = store.getters['auth/user'];
            if (user.is_staff) {
              next(`/batch/${to.params.id}/qa`);
            } else {
              next(`/batch/${to.params.id}/annotate`);
            }
          },
          props: route => ({ batchId: route.params.id }),
        },
        {
          path: 'annotate',
          component: Annotate,
          props: route => ({ batchId: route.params.id }),
        },
        {
          path: 'stats',
          component: Stats,
          props: route => ({ batchId: route.params.id }),
        },
        {
          path: 'qa',
          component: QA,
          props: route => ({ batchId: route.params.id }),
        },

        {
          path: 'review',
          component: Review,
          props: route => ({ batchId: route.params.id }),
        },
      ],
    },
    //  { path: '*', redirect: '/projects' }
  ],
});

router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const isAuthenticated = store.getters['auth/isAuthenticated'];

  if (authRequired && !isAuthenticated) {
    return next('/login');
  }

  if (isAuthenticated && to.name === 'login') {
    return next('projects');
  }

  return next();
});

export default router;
