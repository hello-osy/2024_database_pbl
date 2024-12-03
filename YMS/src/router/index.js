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
  
  // 인증되지 않은 사용자가 로그인이나 회원가입 페이지로 접근하면 허용
  if (to.name === 'login' || to.name === 'SignUp') {
    next(); // 회원가입 및 로그인 페이지로의 이동 허용
  } else if (!isAuthenticated) {
    next({ name: 'login' }); // 인증되지 않은 사용자는 로그인 페이지로 리다이렉트
  } else {
    next(); // 인증된 사용자는 이동 허용
  }
});


export default router;