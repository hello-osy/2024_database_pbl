<template>
  <div class="signup-container">
    <!-- 박스 내부 -->
    <form @submit.prevent="handleSignUp">
      <!-- 중앙에 보이는 이미지 -->
      <div class="login-page-logo">
        <img src="@/assets/img/onepiece-logo-word.png" alt="Logo" />
      </div>

      <!-- 입력 필드 -->
      <label for="role">Role</label>
      <select id="role" v-model="role" required>
        <option disabled value="">Select a role</option> <!-- 선택 강제 -->
        <option value="1">Manager</option>
        <option value="2">Driver</option>
      </select>

      <label for="username">Username</label>
      <input type="text" id="username" v-model="username" required />

      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" required />

      <!-- 회원가입 버튼 -->
      <button type="submit">Sign Up</button>
    </form>

    <!-- 로그인 링크 -->
    <router-link to="/">Already have an account? Log in</router-link>
  </div>
</template>



<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      role: "",
    };
  },
  methods: {
    async handleSignUp() {
      // 입력된 데이터 콘솔에 출력
      console.log("Sign-up attempt with:");
      console.log("Username:", this.username);
      console.log("Password:", this.password);
      console.log("Role ID:", this.role, "(Type:", typeof this.role, ")");
      try {
        const response = await axios.post("http://localhost:8080/api/signup", {
          username: this.username,
          password: this.password,
          role_id: this.role,
        });

        if (response.data.success) {
          alert("Sign-up successful!");
          this.$router.push({ name: "login" });
        } else {
          alert(response.data.message || "Sign-up failed");
        }
      } catch (error) {
        console.error("Sign-up error:", error);
        alert("An error occurred during sign-up");
      }
    },
  },
};
</script>

<style></style>