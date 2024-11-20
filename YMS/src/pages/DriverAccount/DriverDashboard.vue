<template>
    <div class="dashboard">
      <!-- Header Section -->
      <div class="header">
        <h1>Welcome, {{ driver.name }}!</h1>
        <p class="status">
          Current Status: 
          <span :class="statusClass">{{ driver.status }}</span>
        </p>
        <button @click="toggleStatus">{{ toggleStatusText }}</button>
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
  
      <!-- Notifications Section -->
      <div class="notifications">
        <h2>Notifications</h2>
        <ul>
          <li v-for="notification in notifications" :key="notification.id">
            {{ notification.message }}
          </li>
        </ul>
      </div>
    </div>
  </template>

<script>
export default {
  data() {
    return {
      driver: {
        name: "John Doe",
        status: "Available", // Status: Available, On a Trip, Offline
      },
      metrics: [
        { label: "Trips Completed", value: 120 },
        { label: "Earnings (This Month)", value: "$1,200" },
        { label: "Average Rating", value: "4.8" },
      ],
      upcomingTrip: {
        pickup: "123 Elm Street",
        dropoff: "456 Oak Avenue",
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
      return {
        available: this.driver.status === "Available",
        "on-trip": this.driver.status === "On a Trip",
        offline: this.driver.status === "Offline",
      };
    },
    toggleStatusText() {
      return this.driver.status === "Available" ? "Go Offline" : "Go Online";
    },
  },
  methods: {
    toggleStatus() {
      this.driver.status =
        this.driver.status === "Available" ? "Offline" : "Available";
    },
  },
  mounted() {
    // Initialize the map or fetch live location
    this.initializeMap();
  },
  methods: {
    initializeMap() {
      // Add map logic here (e.g., using Leaflet.js or Google Maps)
      console.log("Initialize map with driver location.");
    },
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

.metrics {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
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

.upcoming-trip,
.map,
.notifications {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.map #map-container {
  height: 300px;
  background: #eee;
}

.notifications ul {
  list-style: none;
  padding: 0;
}

.notifications li {
  margin: 5px 0;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 5px;
}
</style>
