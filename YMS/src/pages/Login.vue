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
export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    handleLogin() {
      // 로컬스토리지에서 사용자 목록 가져오기
      const users = JSON.parse(localStorage.getItem("users")) || [];
      
      // 입력한 사용자 정보로 검색
      const user = users.find(
        (u) => u.username === this.username && u.password === this.password
      );

      if (user) {
        localStorage.setItem("loggedIn", "true");
        if (this.username === "manager001") {
          this.$router.push("/admin/dashboard"); // 매니저 페이지로 이동
        } else if (this.username === "driver001") {
          this.$router.push("/driver/driverdashboard"); // 드라이버 페이지로 이동
        } else {
          this.errorMessage = "No page available for this user.";
        }
      } else {
        this.errorMessage = "Invalid username or password.";
      }
    },
  },
  mounted() {
    // 기본 사용자 계정 추가 (초기화)
    const defaultUsers = [
      { username: "manager001", password: "1234" },
      { username: "driver001", password: "1234" },
    ];

    const users = JSON.parse(localStorage.getItem("users")) || [];
    if (users.length === 0) {
      localStorage.setItem("users", JSON.stringify(defaultUsers));
    }
  },
};
</script>
          <!-- // async login() {
          //   try {
          //     const response = await axios.post('', {
          //       id: this.username,
          //       password: this.password,
          //     });

          //     if (response.data.success) {
          //       const userId = this.username;
          //       const userPw = this.password;

          //       if(userId === "manager001" && this.password === "1234") {
          //         //localStorage.setItem("loggedIn", "ture");
          //         this.$router.push({name: "division"});
          //       }

          //       localStorage.setItem('token', response.data.token);
          //     }
          //     else {
          //       this.errorMessage = "Invalid username or password";
          //     }
          //   } catch (error){
          //     this.errorMessage = error.response?.data?.message || 'An error occuered';
          //   }
          // } -->

<style></style>