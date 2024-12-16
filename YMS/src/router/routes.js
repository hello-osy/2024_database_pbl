import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
import DriverPageLayout from "@/layout/driver/DriverPageLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

//Login page
import Login from "@/pages/Login.vue";
import SignUp from "@/pages/SignUp.vue";

// Admin pages
import DashBoard from "@/pages/Admin/DashBoard.vue";
import DriverList from "@/pages/Admin/DriverList.vue";
import TransportLog from "@/pages/Admin/TransportLog.vue";
import AssignedManagement from "@/pages/Admin/AssignedManagement.vue";

// Admin pages - division
import LApage from "@/pages/Admin/Division/LApage.vue";
import PHXpage from "@/pages/Admin/Division/PHXpage.vue";
import HOUpage from "@/pages/Admin/Division/HOUpage.vue";
import SAVpage from "@/pages/Admin/Division/SAVpage.vue";
import MOBpage from "@/pages/Admin/Division/MOBpage.vue";

// Driver pages
import DriverDashboard from "@/pages/Driver/DriverDashboard.vue";
import DriverProfile from "@/pages/Driver/DriverProfile.vue";
import DriverSchedule from "@/pages/Driver/DriverSchedule.vue";
import EditProfile from "@/pages/Driver/EditProfile.vue";

const routes = [
  {
    path: "/",
    name: "login",
    component: Login,
  },
  {
    path: "/signup",
    name: "SignUp",
    component: SignUp,
  },
  {
    path: "/admin",
    component: DashboardLayout,
    redirect: "/admin/dashboard",
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: DashBoard,
      },
      {
        path: "lapage",
        name: "LApage",
        component: LApage,
        meta: { division: "LA" },
      },
      {
        path: "phxpage",
        name: "PHXpage",
        component: PHXpage,
        meta: { division: "PHX" },
      },
      {
        path: "houpage",
        name: "HOUpage",
        component: HOUpage,
        meta: { division: "HOU" },
      },
      {
        path: "mobpage",
        name: "MOBpage",
        component: MOBpage,
        meta: { division: "MOB" },
      },
      {
        path: "savpage",
        name: "SAVpage",
        component: SAVpage,
        meta: { division: "SAV" },
      },
      {
        path: "driverlist",
        name: "DriverList",
        component: DriverList,
      },
      {
        path: "transportlog",
        name: "transportlog",
        component: TransportLog,
      },
      {
        path: "assignedmanagement",
        name: "AssignedManagement",
        component: AssignedManagement,
      },
    ],
  },
  {
    path: "/driver",
    component: DriverPageLayout,
    redirect: "/driver/driverdashboard",
    children: [
      {
        path: "driverdashboard",
        name: "DriverDashboard",
        component: DriverDashboard,
      },
      {
        path: "driverprofile",
        name: "DriverProfile",
        component: DriverProfile,
      },
      {
        path: "driverschedule",
        name: "DriverSchedule",
        component: DriverSchedule,
      },
      {
        path: "editprofile",
        name: "EditProfile",
        component: EditProfile,
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
