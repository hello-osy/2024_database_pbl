<template>
  <div class="profile-page">
    <!-- Header Section -->
    <div class="header">
      <div class="profile-picture">
        <!-- Display Asset Image -->
        <label for="upload-picture">
          <img
            :src="driver.picture"
            alt="Driver Profile Picture"
            class="profile-image"
          />
        </label>
        <!-- Upload Button -->
        <input
          type="file"
          id="upload-picture"
          accept="image/*"
          @change="onImageChange"
          style="display: none;"
        />
      </div>
      <h1>  {{ driver.name }}</h1>
      <p> Click on the picture for change profile-picture</p>
      <br />
    </div>

    <!-- Personal Information Section -->
    <div class="info-section">
      <h2>Personal Information</h2>
      <ul>
        <li><strong>Phone:</strong> {{ driver.phone }}</li>
        <li><strong>Email:</strong> {{ driver.email }}</li>
        <li><strong>Address:</strong> {{ driver.address }}</li>
      </ul>
    </div>

    <!-- Professional Information Section -->
    <div class="info-section">
      <h2>Professional Information</h2>
      <ul>
        <li><strong>Assigned Vehicle:</strong> {{ driver.vehicle }}</li>
        <li><strong>License Plate:</strong> {{ driver.licensePlate }}</li>
        <li><strong>Trips Completed:</strong> {{ stats.tripsCompleted }}</li>
        <li><strong>Average Rating:</strong> {{ stats.rating }}</li>
      </ul>
    </div>

    <!-- Action Buttons -->
    <div class="actions">
      <button @click="navigateToEditProfile">Edit My Profile</button>
    </div>
  </div>
</template>

<script>

import driverImage from "@/assets/img/driver-profile03.png";

export default {
  data() {
    return {
      driver: {
        name: "John Doe",
        picture: require("@/assets/img/driver-profile03.png"), // Load asset image using require
        phone: "123-456-7890",
        email: "john.doe@example.com",
        address: "123 Elm Street, Springfield",
        vehicle: "Truck",
        licensePlate: "XYZ-123",
        status: "Available",
      },
      stats: {
        tripsCompleted: 120,
        rating: 4.8,
      },
    };
  },
  methods: {
    onImageChange(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.driver.picture = e.target.result; // Update the picture with the uploaded image
        };
        reader.readAsDataURL(file); // Convert image to base64 for preview
      }
    },
    navigateToEditProfile() {
      this.$router.push({ name: "EditProfile" });
    },
  },
};
</script>


<style scoped>
.profile-page {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.header {
  text-align: center;
}

.profile-picture {
  position: relative;
}

.profile-picture img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  border: 2px solid #ddd;
  cursor: pointer;
  object-fit: cover;
}

/* Info Box CSS */
.info-section {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}
.info-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}


.info-section h2 {
  margin-bottom: 10px;
}

.info-section ul {
  list-style-type: none;
  padding: 0;
}

.info-section li {
  margin-bottom: 5px;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

.actions button {
  margin: 5px;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
}
/* buttons */
  button {
      width: 200px;
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

/*Personal and Professional Information Section  */
.info-section {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8pxinfo-section;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.info-section h2 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
  font-family: 'Arial', sans-serif;
  text-transform: uppercase;
}

.info-section p {
  font-size: 16px;
  margin: 5px 0;
  line-height: 1.5;
  color: #555;
}

.info-section strong {
  color: #333;
}

.upcoming-trip:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.info-section div {
  padding: 10px 0;
}

.info-section p {
  animation: fadeIn 1s ease-in-out;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }

}
</style>