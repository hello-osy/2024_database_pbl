import Vue from "vue";
import VueRouter from "vue-router";
import routes from "./routes";
Vue.use(VueRouter);

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: "active",
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('loggedIn');
  if (to.name !== 'login' && !isAuthenticated) {
    next({ name: 'login' }); // 로그인 페이지로 리다이렉트
  } else {
    next(); // 이동 허용
  }
});

export default router;