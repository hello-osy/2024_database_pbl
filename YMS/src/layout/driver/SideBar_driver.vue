<template>
  <div class="sidebar-driver">
    <ul class="sidebar-menu">
      <li>
        <router-link to="/driver/Dashboard">
          <i class="ti-user"></i> Dashboard
        </router-link>
      </li>
      <li>
        <router-link to="/driver/profile">
          <i class="ti-user"></i> Profile
        </router-link>
      </li>
      <li>
        <router-link to="/driver/schedules">
          <i class="ti-calendar"></i> Schedule
        </router-link>
      </li>
      <li>
        <router-link to="/driver/edit-profile">
          <i class="ti-settings"></i> Edit Profile
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "SideBarDriver",
};
</script>

<style scoped>
.sidebar-driver {
  width: 200px;
  height: 100vh;
  background-color: #343a40;
  color: white;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-menu li {
  margin:70px 0;
}

.sidebar-menu li a {
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.sidebar-menu li a:hover {
  color: #f8f9fa;
}

.sidebar-menu li a i {
  margin-right: 10px;
}
</style>