<template>
  <div class="profile-page">
    <!-- Header Section -->
    <div class="header">
      <div class="profile-picture">
        <img :src="driver.picture" alt="Driver Profile Picture" />
      </div>
      <h1>{{ driver.name }}</h1>
      <p class="status">{{ driver.status }}</p>
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
      <button @click="editProfile">Edit Profile</button>
      <button @click="contactSupport">Contact Support</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      driver: {
        name: "John Doe",
        picture: "https://via.placeholder.com/150", // Placeholder image
        phone: "123-456-7890",
        email: "john.doe@example.com",
        address: "123 Elm Street, Springfield",
        vehicle: "Toyota Prius",
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
    editProfile() {
      // Navigate to edit profile page or open a modal
      console.log("Edit Profile clicked");
    },
    contactSupport() {
      // Open a support contact form or display information
      console.log("Contact Support clicked");
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

.profile-picture img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.status {
  font-style: italic;
  color: green;
}

.info-section {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
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
</style>


