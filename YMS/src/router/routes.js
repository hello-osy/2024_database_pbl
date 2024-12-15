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
import YardVisualization from "../pages/Admin/YardVisualization.vue";
import Yard1 from "@/pages/Admin/Yard/Yard1.vue";
import Yard2 from "@/pages/Admin/Yard/Yard2.vue";
import Yard3 from "@/pages/Admin/Yard/Yard3.vue";
import Yard4 from "@/pages/Admin/Yard/Yard4.vue";
import Yard5 from "@/pages/Admin/Yard/Yard5.vue";
import Yard6 from "@/pages/Admin/Yard/Yard6.vue";
import Yard7 from "@/pages/Admin/Yard/Yard7.vue";
import Yard8 from "@/pages/Admin/Yard/Yard8.vue";
import Yard9 from "@/pages/Admin/Yard/Yard9.vue";
import Yard10 from "@/pages/Admin/Yard/Yard10.vue";

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
    redirect: "/division",
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        component: DashBoard,
      },
      {
        path: "yard-visualization",
        name: "YardVisualization",
        component: YardVisualization,
      },
      {
        path: "yard1",
        name: "yard1",
        component: Yard1,
      },
      {
        path: "yard2",
        name: "yard2",
        component: Yard2,
      },
      {
        path: "yard3",
        name: "yard3",
        component: Yard3,
      },
      {
        path: "yard4",
        name: "yard4",
        component: Yard4,
      },
      {
        path: "yard5",
        name: "yard5",
        component: Yard5,
      },
      {
        path: "yard6",
        name: "yard6",
        component: Yard6,
      },
      {
        path: "yard7",
        name: "yard7",
        component: Yard7,
      },
      {
        path: "yard8",
        name: "yard8",
        component: Yard8,
      },
      {
        path: "yard9",
        name: "yard9",
        component: Yard9,
      },
      {
        path: "yard10",
        name: "yard10",
        component: Yard10,
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
