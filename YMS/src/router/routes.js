import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";

// Driver Page 
import DriverPageLayout from "@/layout/driver/DriverPageLayout.vue";

// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Login page
import Login from "@/pages/Login.vue";

// Admin pages
import Dashboard from "@/pages/Dashboard.vue";
import Icons from "@/pages/Icons.vue";
import DivisionPage from "@/pages/Division.vue";
import DriverProfiles from "@/pages/DriverProfiles.vue";
import TransportLog from "@/pages/TransportLog.vue";
import Yard1 from "@/pages/Yard/Yard1.vue";
import Yard2 from "@/pages/Yard/Yard2.vue";
import Yard3 from "@/pages/Yard/Yard3.vue";
import AssignedManagement from "@/pages/AssignedManagement.vue";
import DriverProfile from "../pages/DriverAccount/DriverProfile.vue";
import DriverDashboard from "../pages/DriverAccount/DriverDashboard.vue";
import DriverSchedule from "../pages/DriverAccount/DriverSchedule.vue";

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
        path: "/yard1",
        name: "yard1",
        component: Yard1,
      },
      {
        path: "/yard2",
        name: "yard2",
        component: Yard2,
      },
      {
        path: "/yard3",
        name: "yard3",
        component: Yard3,
      },
      {
        path: "/dashboard",
        name: "dashboard",
        component: Dashboard,
      },
      {
        path: "/driver-profiles",
        name: "driverprofiles",
        component: DriverProfiles,
      },
      {
        path: "/transport-log",
        name: "transprot-log",
        component: TransportLog,
      },
      {
        path: "/icons",
        name: "icons",
        component: Icons,
      },
      {
        path: "/assigned-management",
        name: "assigned-management",
        component: AssignedManagement,
      },
    ],
  },
  {
    path: '/driver', // Base path for DriverPageLayout
    component: DriverPageLayout,
    redirect: '/driver/dashboard',
    children: [ 
      {
        path: 'profile', // Nested path (e.g., /driver/profile)
        name: 'DriverProfile',
        component: DriverProfile
      },
      {
        path: 'dashboard',
        name: 'DriverDashboard',
        component: DriverDashboard
      },
      {
        path: 'schedules',
        name: 'DriverSchedule',
        component: DriverSchedule
      }
    ]
  },
  { path: "*", component: NotFound },
];

export default routes;
