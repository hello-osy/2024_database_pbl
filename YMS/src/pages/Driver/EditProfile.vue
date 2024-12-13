<template>
    <div class="edit-profile-container">
      <h1>Edit Profile</h1>
      <form @submit.prevent="handleSubmit">
        <label>Email:</label>
        <input type="email" required v-model="email" />
  
        <label>Password:</label>
        <input type="password" required v-model="password" />
        <div v-if="passwordError" class="error">{{ passwordError }}</div>
  
        <label>License Plate:</label>
        <input
          type="text"
          required
          v-model="licensePlate"
          @input="validateLicensePlate"
        />
        <div v-if="licensePlateError" class="error">{{ licensePlateError }}</div>
  
        <!-- Select Box for Truck Type -->
        <label>Truck Type:</label>
        <select v-model="truckType" required>
          <option value="" disabled>Select truck type</option>
          <option value="private">Private truck</option>
          <option value="company">Company truck</option>
        </select>
        <div v-if="truckTypeError" class="error">{{ truckTypeError }}</div>
  
        <label>Phone Number:</label>
        <input
          type="text"
          required
          v-model="phoneNumber"
          @input="validatePhoneNumber"
        />
        <div v-if="phoneError" class="error">{{ phoneError }}</div>
  
        <div class="terms">
          <input type="checkbox" required v-model="terms" />
          <label>Accept terms and conditions</label>
          <div v-if="termsError" class="error">{{ termsError }}</div>
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
        email: "",
        password: "",
        licensePlate: "",
        truckType: "", // Truck type select box value
        phoneNumber: "",
        terms: false,
        passwordError: "",
        licensePlateError: "",
        truckTypeError: "",
        phoneError: "",
        termsError: "",
      };
    },
    methods: {
      validatePhoneNumber() {
        const phoneRegex = /^[0-9]{10,15}$/; // Example: 10-15 digits
        this.phoneError = phoneRegex.test(this.phoneNumber)
          ? ""
          : "Invalid phone number.";
      },
      validateLicensePlate() {
        const licensePlateRegex = /^[A-Za-z0-9\s-]{1,10}$/; // Adjust pattern as needed
        this.licensePlateError = licensePlateRegex.test(this.licensePlate)
          ? ""
          : "Invalid license plate format.";
      },
      handleSubmit() {
        this.passwordError =
          this.password.length < 4
            ? "Password must be at least 4 characters long."
            : "";
  
        this.licensePlateError = this.licensePlate ? "" : "License plate is required.";
        this.truckTypeError = this.truckType ? "" : "Please select a truck type.";
        this.termsError = this.terms ? "" : "You must accept the terms.";
  
        if (
          !this.passwordError &&
          !this.licensePlateError &&
          !this.truckTypeError &&
          !this.phoneError &&
          !this.termsError
        ) {
          console.log("Email:", this.email);
          console.log("Password:", this.password);
          console.log("License Plate:", this.licensePlate);
          console.log("Truck Type:", this.truckType);
          console.log("Phone Number:", this.phoneNumber);
          alert("Information saved successfully!");
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
     input, select {
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