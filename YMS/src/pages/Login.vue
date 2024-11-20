<template>
    <div class="login-container">
        <h1>Sign In</h1>
        <div class="login-box">
            <form @submit.prevent="handleLogin">
                <label for="role">Role:</label>
                <select v-model="role" id="role" required>
                  <option value="manager">Manager</option>
                  <option value="driver">Driver</option>
                </select>
                <br />
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required />
                <br />
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
                <br />
                <button type="submit">Sign In</button>
              </form>
              <p v-if="errorMessage" id="errorMessage">{{ errorMessage }}</p>
        </div>
    </div>
</template>

<script>
//import axios from 'axios'
    export default {
        data() {
          return {
            role: "",
            username: "",
            password: "",
            errorMessage: "",
          };
        },
        // mounted() {
        //   const link = document.createElement("link");
        //   link.rel = "stylesheet";
        //   link.href = "@/assets/css/signin.css"; // signin.css의 실제 경로로 변경
        //   link.id = "signin-styles"; // 나중에 제거할 수 있도록 ID 추가
        //   document.head.appendChild(link);
        // },
        // beforeDestroy() {
        //   const link = document.getElementById("signin-styles");
        //   if (link) {
        //     document.head.removeChild(link); // 컴포넌트가 제거되면 스타일도 제거
        //   }
        // },
        methods: {
          handleLogin() {
            if (this.role === "manager" && this.username === "manager001" && this.password === "1234") {
              localStorage.setItem("loggedIn", "true"); // 인증 상태 저장
              this.$router.push({name: "division"}); // 관리자 페이지로 이동
            } else if (this.role === "driver" && this.username === "driver001" && this.password === "1234") {
              localStorage.setItem("loggedIn", "true");
              this.$router.push({name: "DriverProfile"});  // 드라이버 페이지로 이동
            } else {
              this.errorMessage = "Invalid username or password.";
            }
          },
          // async login() {
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
          // }
        },
      };
</script>

<style scoped>
  /* 기본 스타일 */
  body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f4f4f4;
  }

  /* 로그인 페이지 스타일 */
  .login-container {
      text-align: center;
  }

  .login-box {
      background-color: #fff;
      padding: 40px;
      border-radius: 10px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
      width: 350px;
  }

  h1 {
      font-size: 32px;
      margin-bottom: 20px;
  }

  label {
      font-size: 18px;
      margin: 15px 0 5px;
      display: block;
  }

  input, select {
      width: 100%;
      padding: 12px;
      margin-bottom: 20px;
      border: 1px solid #ccc;
      border-radius: 5px;
      font-size: 16px;
  }

  button {
      width: 100%;
      padding: 15px;
      background-color: #4CAF50;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 18px;
  }

  button:hover {
      background-color: #45a049;
  }

  #errorMessage {
      color: red;
      margin-top: 10px;
  }
</style>