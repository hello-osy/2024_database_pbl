// src/router/index.js
import Vue from "vue";
import Router from "vue-router";
import Division from '@/pages/Division.vue';
import Yard1 from "@/pages/Yard1.vue";
import Yard2 from "@/pages/Yard2.vue";
import Yard3 from "@/pages/Yard3.vue";
import TransportLog from "@/pages/TransportLog.vue";
import DriverProfiles from "@/pages/DriverProfiles.vue";

Vue.use(Router);

export default new Router({
  mode: 'hash', // hash 모드 설정
  routes: [
    {
      path: '/',
      redirect: '/division', // 기본 경로를 Division 페이지로 리디렉션
    },
    {
      path: '/division',
      name: "Division", 
      component: Division
    },
    {
      path: "/yard1",
      name: "Yard1",
      component: Yard1,
    },
    {
      path: "/yard2",
      name: "Yard2",
      component: Yard2,
    },
    {
      path: "/yard3",
      name: "Yard3",
      component: Yard3,
    },
    {
      path: "/transport-log",
      name: "Transport Log",
      component: TransportLog,
    },
    {
      path: "/driver-profiles",
      name: "Driver Profiles",
      component: DriverProfiles,
    },
    {
      path: "*",
      redirect: "/division", // 잘못된 경로는 Division 페이지로 리디렉션
    },
  ],
});
