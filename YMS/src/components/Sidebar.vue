<!-- src/components/Sidebar.vue -->
<template>
    <div class="sidebar">
      <ul class="sidebar-menu">
        <!-- Division 메뉴 -->
        <li
          class="menu-item has-submenu"
          @mouseenter="showDivisionMenu"
          @mouseleave="hideDivisionMenu"
        >
          <!-- Division 메뉴 클릭 시 페이지 이동 -->
          <router-link to="/division" class="submenu-title" @click="goToDivision">
            <i class="ti-layout-grid3"></i>
            <span>Division</span>
          </router-link>
  
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
  
        <!-- Assigned Management 메뉴 추가 -->
        <li class="menu-item">
          <router-link to="/assigned-management">
            <i class="ti-clipboard"></i>
            <span>Assigned Management</span>
          </router-link>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: "Sidebar",
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
      showDivisionMenu() {
        this.divisionMenuOpen = true; // Division 하위 메뉴 표시
      },
      hideDivisionMenu() {
        this.divisionMenuOpen = false; // Division 하위 메뉴 숨기기
      },
      goToDivision() {
        // Division 메뉴 클릭 시 하위 메뉴 열림을 방지하고 Division.vue로 이동
        this.$router.push("/division");
        this.hideDivisionMenu(); // Division 페이지로 이동 후 하위 메뉴 숨기기
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
    position: absolute;
    top: 100%;
    left: 0;
    background-color: #343a40;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    border-radius: 4px;
    padding: 10px 0;
    list-style-type: none;
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.3s ease, visibility 0.3s ease;
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
  }
  
  /* 마우스 올릴 때 하위 메뉴 보이기 */
  .menu-item.has-submenu:hover .submenu {
    visibility: visible;
    opacity: 1;
    transition: opacity 0.3s ease, visibility 0.3s ease;
  }
  </style>
  