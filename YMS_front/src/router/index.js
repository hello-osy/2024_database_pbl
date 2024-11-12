// src/router/index.js
import Vue from "vue";
import Router from "vue-router";
import Yard1 from "@/pages/Yard1.vue";
import Yard2 from "@/pages/Yard2.vue";
import Yard3 from "@/pages/Yard3.vue";
import TransportLog from "@/pages/TransportLog.vue";
import DriverProfiles from "@/pages/DriverProfiles.vue";

Vue.use(Router);

export default new Router({
  routes: [
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
      redirect: "/yard1",
    },
  ],
});
