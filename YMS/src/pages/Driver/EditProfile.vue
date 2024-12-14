<template>
  <div class="edit-profile-container">
    <h1>Edit Profile</h1>
    <form @submit.prevent="handleSubmit">
      <label> Email: </label>
      <input type="email" required v-model="email" />

      <label> Password: </label>
      <input type="password" required v-model="password" />
      <div v-if="passwordError" class="error">{{ passwordError }}</div>

      <label>Phone Number:</label>
      <input type="text" v-model="phone" placeholder="Enter phone number" />

      <label>Address:</label>
      <input type="text" v-model="address" placeholder="Enter address" />

      <label>Private Truck Info:</label>
      <input
        type="text"
        v-model="privateTruckInfo"
        placeholder="Enter truck info"
      />

      <div class="terms">
        <input type="checkbox" required v-model="terms" />
        <label> Accept terms and conditions </label>
      </div>

      <div class="submit">
        <button type="submit">Save</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "", // Email 입력값
      password: "", // Password 입력값
      phone: "", // Phone Number 입력값
      address: "", // Address 입력값
      privateTruckInfo: "", // Private Truck Info 입력값
      terms: false, // 약관 동의 여부
      passwordError: "", // 비밀번호 유효성 검증 메시지
    };
  },
  methods: {
    async handleSubmit() {
      console.log("Email:", this.email);
      console.log("Password:", this.password);
      console.log("Phone Number:", this.phone);
      console.log("Address:", this.address);
      console.log("Private Truck Info:", this.privateTruckInfo);

      const response = await fetch("http://localhost:8080/api/update-profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({
          email: this.email,
          phone: this.phone,
          address: this.address,
          privateTruckInfo: this.privateTruckInfo,
          password: this.password,
        }),
      });

      const data = await response.json();
      console.log("Response:", data);
      if (data.success) {
        alert("Profile updated successfully!");
      } else {
        console.error("Error:", data.message);
      }
    },
  },
};
</script>

<style scoped>
form {
  max-width: 420px;
  margin: 30px auto;
  background: white;
  text-align: left;
  padding: 40px;
  border-radius: 10px;
}
label {
  color: #aaa;
  display: inline-block;
  margin: 25px 0 15px;
  font-size: 0.6em;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}
input {
  display: block;
  padding: 10px 6px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  border-bottom: 1px solid #ddd;
  color: #555;
}
input,
select {
  display: block;
  padding: 10px 6px;
  width: 100%;
  box-sizing: border-box;
  border: none;
  border-bottom: 1px solid #ddd;
  color: #555;
}
input[type="checkbox"] {
  display: inline-block;
  width: 16px;
  margin: 0 10px 0 0;
  position: relative;
  top: 2px;
}
.pill {
  display: inline-block;
  margin: 20px 10px 0 0;
  padding: 6px 12px;
  background: #eee;
  border-radius: 20px;
  font-size: 12px;
  letter-spacing: 1px;
  font-weight: bold;
  color: #777;
  cursor: pointer;
}
button {
  width: 150px;
  padding: auto;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
}

button:hover {
  background-color: #45a049;
}
.submit {
  text-align: center;
}
.error {
  color: #ff0062;
  margin-top: 10px;
  font-size: 0.8em;
  font-weight: bold;
}
</style>
