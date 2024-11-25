<template>
  <div class="dashboard">
    <!-- Header Section -->
    <div class="header">
      <h1>Welcome, {{ driver.name }}!</h1>
      <p class="status">
        Current Status:
        <span :class="statusClass">{{ driver.status }}</span>
      </p>
        <button class="status-button" @click="changeStatus">{{ toggleStatusText }}</button>
    </div>

    <!-- Metrics Section -->
    <div class="metrics">
      <div class="card" v-for="metric in metrics" :key="metric.label">
        <h3>{{ metric.value }}</h3>
        <p>{{ metric.label }}</p>
      </div>
    </div>

    <!-- Upcoming Trip Section -->
    <div class="upcoming-trip">
      <h2>Upcoming Trip</h2>
      <div v-if="upcomingTrip">
        <p><strong>Pickup:</strong> {{ upcomingTrip.pickup }}</p>
        <p><strong>Drop-off:</strong> {{ upcomingTrip.dropoff }}</p>
        <p><strong>Time:</strong> {{ upcomingTrip.time }}</p>
      </div>
      <div v-else>
        <p>No upcoming trips scheduled.</p>
      </div>
    </div>

    <!-- Map Section -->
    <div class="map">
      <h2>Current Location</h2>
      <div id="map-container"></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      driver: {
        name: "John Doe",
        status: "Available", // Default status
        statuses: [
          { status: "Available" },
          { status: "On a Trip" },
          { status: "Offline" },
        ],
      },
      metrics: [
        { label: "Trips completed", value: 120 },
        { label: "Earnings (This Month)", value: "$19,000" },
        { label: "Average Rating", value: 4.8 },
      ],
      upcomingTrip: {
        pickup: "123 Elm Street",
        dropoff: "426 Oak Avenue",
        time: "Tomorrow, 10:00 AM",
      },
      notifications: [
        { id: 1, message: "Your next trip is scheduled for tomorrow." },
        { id: 2, message: "New earnings report available." },
      ],
    };
  },
  computed: {
    statusClass() {
      // Dynamically assign classes based on driver status
      return {
        available: this.driver.status === "Available",
        "on-trip": this.driver.status === "On a Trip",
        offline: this.driver.status === "Offline",
      };
    },
    toggleStatusText() {
      // Change button text based on driver status
      return this.driver.status === "Available" ? "Go Offline" : "Go Online";
    },
  },
  methods: {
    changeStatus() {
      // Toggle driver status between Available and Offline
      this.driver.status =
        this.driver.status === "Available" ? "Offline" : "Available";
      console.log("Status changed:", this.driver.status);
    },
    initializeMap() {
      // Add map initialization logic here
      console.log("Initialize map with driver location.");
    },
  },
  mounted() {
    // Initialize the map or fetch live location
    this.initializeMap();
  },
};
</script>


<style scoped>
.dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: auto;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.status {
  font-size: 18px;
}

.status span {
  font-weight: bold;
}

.status .available {
  color: green;
}

.status .on-trip {
  color: orange;
}

.status .offline {
  color: red;
}

/* Metrics status */
.metrics {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  cursor: pointer;
}
.metrics:hover{
  transform: scale(1.1); /* Slightly increase size on hover */

}

.card {
  flex: 1;
  background: #f8f9fa;
  padding: 20px;
  text-align: center;
  margin: 0 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Upcoming Trip */
.upcoming-trip {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.upcoming-trip h2 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
  font-family: 'Arial', sans-serif;
  text-transform: uppercase;
}

.upcoming-trip p {
  font-size: 16px;
  margin: 5px 0;
  line-height: 1.5;
  color: #555;
}

.upcoming-trip strong {
  color: #333;
}

.upcoming-trip:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.upcoming-trip div {
  padding: 10px 0;
}

/* Add animation to "No upcoming trips scheduled" */
.upcoming-trip p {
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

.map{
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.map #map-container {
  height: 300px;
  background: #eee;
}

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
</style>
