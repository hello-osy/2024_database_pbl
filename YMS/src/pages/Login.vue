<template>
  <div class="login-container">
    <div class="login-box">
      <form @submit.prevent="handleLogin">
        <label class="login-page-logo">
          <img src="@/assets/img/onepiece-logo-word.png" />
        </label>
        <br />
        <label for="username"></label>
        <input
          type="text"
          id="username"
          v-model="username"
          required
          placeholder="Username"
        />
        <br />
        <label for="password"></label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          placeholder="Password"
        />
        <br />
        <p v-if="errorMessage" id="errorMessage">{{ errorMessage }}</p>
        <button type="submit">Sign In</button>
      </form>
      <div class="additional-links">
        <p>
          <router-link to="/forgot-credentials">Forgot your Username or Password?</router-link>
        </p>
        <p>
          <span>Don’t have an account? </span>
          <router-link to="/signup">Sign up</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      try{
        const response = await axios.post('http://localhost:8080/api/login', {
          username: this.username,
          password: this.password,
        });
        if (response.data.success) {
          // JWT 토큰과 사용자 ID 저장
          const token = response.data.token;
          const userId = response.data.user_id;

          localStorage.setItem("token", token);
          localStorage.setItem("user_id", userId);
          localStorage.setItem("loggedIn", "true");

          // Role에 따라 리다이렉트
          if (response.data.role_id === 1) {
            this.$router.push("/admin/dashboard"); // 매니저 페이지로 이동
          } else if (response.data.role_id === 2) {
            this.$router.push("/driver/driverdashboard"); // 드라이버 페이지로 이동
          }
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (error){
        this.errorMessage = "Error occured during login"
      }
    },
  },
};
</script>


<style></style>