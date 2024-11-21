<template>
    <footer class="footer">
      <div class="container-fluid d-flex flex-wrap justify-content-between">
        <nav>
          <ul>
            <li>
              <router-link :to="{ path: '/driver/dashboard' }">Dashboard</router-link>
            </li>
          </ul>
        </nav>
        <div class="copyright d-flex flex-wrap">
          &copy; Created 
          <i class="fa fa-heart heart"></i> by
          <a href="https://github.com/hello-osy/2024_database_pbl" target="_blank">
            &nbsp; One Piece Team</a
          >&nbsp; 2024
        </div>
      </div>
    </footer>
  </template>
  <script>
  export default {};
  </script>
  <style></style>
  