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
      <select id="role" v-model="role" required @change="resetDriverFields">
        <option disabled value="">Select a role</option> <!-- 선택 강제 -->
        <option value="1">Manager</option>
        <option value="2">Driver</option>
      </select>

      <label for="username">Username</label>
      <input type="text" id="username" v-model="username" required />

      <label for="password">Password</label>
      <input type="password" id="password" v-model="password" required />

      <!-- 드라이버만 작성할 필드 -->
      <template v-if="role === '2'">
        <label for="DriverPhone">Phone Number</label>
        <input type="text" id="DriverPhone" v-model="DriverPhone" placeholder="Enter phone number" />

        <label for="Division"> Division Name</label>
        <select name="Division" id="Division" v-model="Division">
          <option disabled value="Select a division name"></option>
          <option value="1">LA</option>
          <option value="2">PHX</option>
          <option value="3">HOU</option>
          <option value="4">MOB</option>
          <option value="5">SAV</option>
        </select>

        <label for="TruckInfo">Truck Info</label>
        <select name="TruckInfo" id="TruckInfo" v-model="TruckInfo">
          <option disabled value="Select your truck info"></option>
          <option value="1">Private truck</option>
          <option value="2">Company truck</option>
        </select>
      </template>

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
      // 드라이버 전용 필드 추가
      DriverPhone: "",
      Division: "",
      TruckInfo: "",
    };
  },
  methods: {
    resetDriverFields(){
      // 역할 변경시 드라이버 필드 뜬다
      if(this.role !== '2'){
        this.Division = " ";
        this.TruckInfo = " ";
        this.DriverPhone = " ";
      }
    },
    async handleSignUp() {
      // 입력된 데이터 콘솔에 출력
      console.log("Sign-up attempt with:");
      console.log("Username:", this.username);
      console.log("Password:", this.password);
      console.log("Role ID:", this.role, "(Type:", typeof this.role, ")");
      console.log("Phone: ", this.DriverPhone)
      console.log("Division: ", this.Division);
      console.log("TruckInfo: ", this.TruckInfo);
      console.log("")

      // 기본 회원가입 데이터
      const signupData = {
        username: this.username,
        password: this.password,
        role_id: this.role
      };

      // 드라이버 전용 데이터
      if (this.role === '2'){
        signupData.driver_phone = this.DriverPhone;
        signupData.division = this.Division;
        signupData.truck_info = this.TruckInfo;
      }

      // Sign Up Request 보내기
      try {
        const response = await axios.post("http://localhost:8080/api/signup", signupData);

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

<style>

</style>