<!-- src/components/Sidebar.vue -->
<template>
    <div class="sidebar">
      <ul class="sidebar-menu">
        <!-- Yard1 메뉴 -->
        <li class="menu-item">
          <router-link to="/yard1">
            <i class="ti-layout-grid3"></i>
            <span>Yard 1</span>
          </router-link>
        </li>
  
        <!-- Yard2 메뉴 -->
        <li class="menu-item">
          <router-link to="/yard2">
            <i class="ti-layout-grid3"></i>
            <span>Yard 2</span>
          </router-link>
        </li>
  
        <!-- Yard3 메뉴 -->
        <li class="menu-item">
          <router-link to="/yard3">
            <i class="ti-layout-grid3"></i>
            <span>Yard 3</span>
          </router-link>
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
    name: "Sidebar",
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
  </style>
  