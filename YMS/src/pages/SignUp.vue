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
        <option value="Manager">Manager</option>
        <option value="Driver">Driver</option>
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
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleSignUp() {
      const newUser = { username: this.username, password: this.password };
      const users = JSON.parse(localStorage.getItem("users")) || [];
      console.log("Before adding new user:", users);

      users.push(newUser);
      localStorage.setItem("users", JSON.stringify(users));

      console.log("After adding new user:", users);
      alert("Sign-up successful!");
      this.$router.push({ name: "login" });
    },
  },
};
</script>
<style></style>