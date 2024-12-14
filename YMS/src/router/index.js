import Vue from "vue";
import VueRouter from "vue-router";
import routes from "./routes";
import axios from "axios";
Vue.use(VueRouter);

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: "active",
});

async function addDynamicRoutes() {
  try {
    console.log("Fetching yard data...");
    const response = await axios.get("/api/yard/all");

    if (response.data.success) {
      const yards = response.data.data;

      // 동적으로 추가할 라우트 배열 생성
      const dynamicRoutes = yards.map((yard) => ({
        path: `/admin/yard/${yard.id}`, // 동적 경로
        name: `Yard${yard.id}`, // 라우트 이름
        component: () => import(`@/pages/Admin/Yard/Yard_reuse.vue`), // Vue 컴포넌트
        meta: { yardName: yard.name, yardId: yard.id }, // 메타 정보
        props: true,
      }));

      // 동적 라우트 추가
      console.log("Adding dynamic routes:", dynamicRoutes);

      router.addRoutes([
        {
          path: "/admin/division",
          component: () => import("@/layout/dashboard/DashboardLayout.vue"),
          children: dynamicRoutes,
        },
      ]);

      console.log("Routes added successfully:", router.options.routes);
    }
  } catch (error) {
    console.error("Failed to fetch yards:", error);
  }
}



// 동적 라우트 추가 후 초기화
addDynamicRoutes();


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