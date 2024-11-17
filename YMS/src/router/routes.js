import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

//Login page
import Login from "@/pages/Login.vue";

// Admin pages
import Dashboard from "@/pages/Dashboard.vue";
import Icons from "@/pages/Icons.vue";
import DivisionPage from "@/pages/Division.vue"
import DriverProfiles from "@/pages/DriverProfiles.vue"
import TransportLog from "@/pages/TransportLog.vue";
import Yard1 from "@/pages/Yard/Yard1.vue"
import Yard2 from "@/pages/Yard/Yard2.vue"
import Yard3 from "@/pages/Yard/Yard3.vue"

const routes = [
  {
    path: "/login",
    name: "login",
    component: Login,
  },
  {
    path: "/",
    component: DashboardLayout,
    redirect: "/division",
    children: [
      {
        path: "division",
        name: "division",
        component: DivisionPage,
      },
      {
        path: "division/yard1",
        name: "yard1",
        component: Yard1,
      },
      {
        path: "division/yard2",
        name: "yard2",
        component: Yard2,
      },
      {
        path: "division/yard3",
        name: "yard3",
        component: Yard3,
      },
      {
        path: "dashboard",
        name: "dashboard",
        component: Dashboard,
      },
      {
        path: "driverprofiles",
        name: "driverprofiles",
        component: DriverProfiles,
      },
      {
        path: "transportlog",
        name: "transprotlog",
        component: TransportLog,
      },
      {
        path: "icons",
        name: "icons",
        component: Icons,
      },
    ],
  },
  { path: "*", component: NotFound },
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes;
