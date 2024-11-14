<!-- src/components/SidebarPlugin/SideBar.vue -->
<template>
  <div class="sidebar">
    <ul class="sidebar-menu">
      <!-- Division 그룹 메뉴 -->
      <li class="menu-item has-submenu">
        <!-- Division 메뉴 클릭 시 페이지 이동 -->
        <router-link to="/division" class="submenu-title">
          <i class="ti-layout-grid3"></i>
          <span>Division</span>
        </router-link>

        <!-- 화살표 아이콘 클릭 시 하위 메뉴 열림/닫힘 -->
        <i
          :class="divisionMenuOpen ? 'ti-angle-down' : 'ti-angle-right'"
          class="submenu-icon"
          @click.stop="toggleDivisionMenu"
        ></i>

        <!-- Division 하위 메뉴 (Yard1, Yard2, Yard3) -->
        <ul v-if="divisionMenuOpen" class="submenu">
          <li class="submenu-item" v-for="yard in yards" :key="yard.path">
            <router-link :to="yard.path">{{ yard.name }}</router-link>
          </li>
        </ul>
      </li>

      <!-- Transport Log 메뉴 -->
      <li class="menu-item">
        <router-link to="/transport-log">
          <i class="ti-list"></i>
          <span>Transport Log</span>
        </router-link>
      </li>

      <!-- Driver Profiles 메뉴 -->
      <li class="menu-item">
        <router-link to="/driver-profiles">
          <i class="ti-user"></i>
          <span>Driver Profiles</span>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "SideBar",
  data() {
    return {
      divisionMenuOpen: false, // Division 서브메뉴 상태
      yards: [
        { name: "Yard 1", path: "/yard1" },
        { name: "Yard 2", path: "/yard2" },
        { name: "Yard 3", path: "/yard3" },
      ],
    };
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
  background-color: #343a40;
  color: #fff;
  height: 100vh;
  position: fixed;
  padding-top: 20px;
}

.sidebar-menu {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.menu-item {
  padding: 15px 20px;
  position: relative;
}

.menu-item a {
  color: #fff;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.menu-item i {
  font-size: 1.2rem;
  margin-right: 10px;
}

.menu-item:hover {
  background-color: #495057;
}

/* 서브메뉴 */
.has-submenu .submenu-title {
  display: flex;
  align-items: center;
}

.submenu {
  list-style-type: none;
  padding-left: 20px;
  margin: 0;
  transition: max-height 0.3s ease;
}

.submenu-item {
  padding: 10px 20px;
}

.submenu-item a {
  color: #ddd;
  font-size: 0.9rem;
}

.submenu-item:hover {
  background-color: #495057;
  padding-left: 25px;
  transition: padding-left 0.2s ease;
}

/* 화살표 아이콘 스타일 */
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
</style>
