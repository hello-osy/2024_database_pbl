import Vue from "vue";
import VueRouter from "vue-router";
import routes from "./routes";
import axios from "axios";
Vue.use(VueRouter);

const laYards=[];
const phxYards=[];
const houYards=[];
const savYards=[];
const mobYards=[];

// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: "active",
});

export async function getYardData(division) {
  try {
    console.log(`${division} 데이터를 가져오고 있습니다.`);
    const response = await axios.get(`/api/yard/${division.toLowerCase()}`);
    console.log(`요청 URL: /api/yard/${division.toLowerCase()}`);
    console.log("서버 응답 데이터:", response.data);

    if(response.data.success) {
      console.log(`${division} 데이터 가져오기 성공`)
      const yards = response.data.data;
      const targetArray =
        division === "LA" ? laYards :
        division === "PHX" ? phxYards : 
        division === "HOU" ? houYards : 
        division === "MOB" ? mobYards : 
        division === "SAV" ? savYards :
        [];

      targetArray.length = 0;
      yards.forEach((yard) => {
        const route = {
          path: `${yard.id}`,
          name: `${yard.id}`,
          component: () => import('@/pages/Admin/Yard/Yard_reuse.vue'),
          meta: {yardName: yard.name, yardId: yard.id, yardLoaction: yard.division_id}
        };
        targetArray.push(route);
        // if (!defaultPages.find((page) => page.path === route.path)) {
        //   defaultPages.push(route);
        // }
      });
      //initializeDefaultRoutes();
      console.log(`${division} 경로 출력:`, targetArray);
    } else {
      console.error(`${division} 데이터를 가져오지 못했습니다.`);
    }
  } catch (error) {
    console.error(`${division} 데이터 가져오기 중 오류 발생:`, error);
  }
}

// 기존 페이지를 DashboardLayout의 children으로 추가
export function initializeDefaultRoutes() {
  const adminRoute = router.options.routes.find((route) => route.path === '/admin');
  if (adminRoute) {
    if (!adminRoute.children) {
      adminRoute.children = [];
    }
    
    const allYards = [...laYards, ...phxYards, ...houYards, ...mobYards, ...savYards];
    console.log("allYard: ", allYards);

    allYards.forEach((page) => {
      if (!adminRoute.children.find((child) => child.name === page.name)) {
        adminRoute.children.push(page);
      }
    });

    // 라우터 갱신
    router.matcher = new VueRouter({
      routes: router.options.routes,
    }).matcher;

    console.log("라우터 초기화 완료: ", adminRoute.children);
  }
}

export function addYard(division) {
  const targetArray = 
    division === "LA" ? laYards :
    division === "PHX" ? phxYards : 
    division === "HOU" ? houYards : 
    division === "MOB" ? mobYards : 
    division === "SAV" ? savYards :
    [];

  const maxId = targetArray.reduce((max, yard) => {
    const match = yard.meta.yardId.match(/\d+$/);
    return match ? Math.max(max, parseInt(match[0])) : max;
  }, 0);
  const newId = `${division}_YARD_${String(maxId + 1).padStart(4, "0")}`;
  const newName = `Yard ${maxId + 1} ${division}`;

  const newYard = {
    path: newId,
    name: newId,
    component: () => import('@/pages/Admin/Yard/Yard_reuse.vue'),
    meta: {
      yardName: newName,
      yardId: newId,
      yardLocation: division,
      addressId: Math.floor(Math.random() * 1000) + 1,
    },
  };
  targetArray.push(newYard);
  console.log(`${division}에 새로운 yard 추가: `, newYard);
  console.log("현재 Target Array: ", targetArray);

  addDynamicRouteToRouter(newYard, division);
}

function addDynamicRouteToRouter(yard, division) {
  const adminRoute = router.options.routes.find((route) => route.path === '/admin');
  if (adminRoute) {
    if (!adminRoute.children) {
      adminRoute.children = []; // children 초기화
    }

    // 중복되지 않으면 children에 추가
    if (!adminRoute.children.find((child) => child.name === yard.name)) {
      adminRoute.children.push(yard);

      // Vue Router matcher 갱신
      router.matcher = new VueRouter({
        routes: router.options.routes,
      }).matcher;

      console.log(`${division} 경로에 새로운 Yard 추가 완료:`, yard);
    }
  }
}

export function getLAYardRoutes() {
  return laYards;
}

export function getPHXYardRoutes() {
  return phxYards;
}

export function getHOUYardRoutes() {
  return houYards;
}

export function getSAVYardRoutes() {
  return savYards;
}

export function getMOBYardRoutes() {
  return mobYards;
}

initializeDefaultRoutes();

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = localStorage.getItem('loggedIn');

  // 로그인과 회원가입 페이지는 인증 체크 없이 허용
  if (to.name === 'login' || to.name === 'SignUp') {
    next(); // 이동 허용
  } else if (!isAuthenticated) {
    next({ name: 'login' }); // 인증되지 않은 사용자는 로그인 페이지로 리다이렉트
  } else {
    // 인증된 사용자일 경우
    if (to.path.startsWith('/admin')) {
      try {
        if (!laYards.length && !phxYards.length && !houYards.length && !mobYards.length && !savYards.length) {
          console.log('Admin 페이지에 진입: 데이터를 로드합니다.');
          await Promise.all([
            getYardData("LA"),
            getYardData("PHX"),
            getYardData("HOU"),
            getYardData("MOB"),
            getYardData("SAV"),
          ]);
          initializeDefaultRoutes(); // 라우트 추가
          console.log("router.options.routes:", router.options.routes);
        }
      } catch (error) {
        console.error('Admin 데이터 로드 중 오류 발생:', error);
      }
    }
    next(); // 인증된 사용자는 이동 허용
  }
});


export default router;