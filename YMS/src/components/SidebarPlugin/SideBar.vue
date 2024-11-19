<template>
  <div
    class="sidebar"
    :data-background-color="backgroundColor"
    :data-active-color="activeColor"
  >
    <div class="sidebar-wrapper" id="style-3">
      <!-- 로고 섹션 -->
      <div class="logo">
        <a href="#" class="simple-text">
          <div class="logo-img">
            <img src="@/assets/img/onepiece_logo.png" alt="" />
          </div>
          {{ title }}
        </a>
      </div>

      <!-- 메뉴 섹션 -->
      <ul class="nav">
        <li class="menu-item has-submenu">
          <!-- Division 메뉴 -->
          <sidebar-link to="/division" name="Division" icon="ti-layout-grid3">
          </sidebar-link>
          <i
            :class="divisionMenuOpen ? 'ti-angle-down' : 'ti-angle-right'"
            class="submenu-icon"
            @click.stop="toggleDivisionMenu"
          ></i>
          <ul v-if="divisionMenuOpen" class="submenu">
            <li class="submenu-item" v-for="yard in yards" :key="yard.path">
              <sidebar-link :to="yard.path" :name="yard.name"></sidebar-link>
            </li>
          </ul>
        </li>

        <!-- Transport Log 메뉴 -->
        <li class="menu-item">
          <sidebar-link
            to="/transport-log"
            name="Transport Log"
            icon="ti-list"
          >
          </sidebar-link>
        </li>

        <!-- Driver Profiles 메뉴 -->
        <li class="menu-item">
          <sidebar-link
            to="/driver-profiles"
            name="Driver Profiles"
            icon="ti-user"
          >
          </sidebar-link>
        </li>

        <!-- Assigned Management 메뉴 -->
        <li class="menu-item">
          <sidebar-link
            to="/assigned-management"
            name="Assigned Management"
            icon="ti-clipboard"
          >
          </sidebar-link>
        </li>
      </ul>

      <!-- Moving Arrow 컴포넌트 -->
      <moving-arrow :move-y="arrowMovePx"></moving-arrow>
    </div>
  </div>
</template>

<script>
import MovingArrow from "./MovingArrow.vue";
import SidebarLink from "./SidebarLink";
export default {
  name: "SideBar",
  props: {
    title: {
      type: String,
      default: "OnePiece YMS",
    },
    backgroundColor: {
      type: String,
      default: "black",
      validator: (value) => ["white", "black", "darkblue"].includes(value),
    },
    activeColor: {
      type: String,
      default: "success",
      validator: (value) =>
        ["primary", "info", "success", "warning", "danger"].includes(value),
    },
  },
  components: {
    MovingArrow,
    SidebarLink,
  },
  data() {
    return {
      divisionMenuOpen: false, // Division 서브메뉴 상태
      yards: [
        { name: "Yard 1", path: "/yard1" },
        { name: "Yard 2", path: "/yard2" },
        { name: "Yard 3", path: "/yard3" },
      ],
      linkHeight: 65,
      activeLinkIndex: 0,
    };
  },
  computed: {
    arrowMovePx() {
      return this.linkHeight * this.activeLinkIndex;
    },
  },
  methods: {
    toggleDivisionMenu() {
      this.divisionMenuOpen = !this.divisionMenuOpen;
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: var(--sidebar-bg-color, #343a40);
  color: var(--sidebar-text-color, #fff);
  height: 100vh;
  position: fixed;
  padding-top: 20px;
}

.nav {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  padding: 15px 20px;
  position: relative;
}

.submenu-icon {
  font-size: 0.9rem;
  cursor: pointer;
  position: absolute;
  right: 15px;
  top: 18px;
  transition: transform 0.3s;
}

.ti-angle-down {
  transform: rotate(180deg);
}

.submenu {
  list-style-type: none;
  padding-left: 20px;
  margin: 0;
}

.submenu-item {
  padding: 10px 20px;
}

.submenu-item:hover {
  background-color: #495057;
  padding-left: 25px;
  transition: padding-left 0.2s ease;
}
</style>
