<template>
  <div class="dashboard">
    <!-- Header Section -->
    <div class="header">
      <h1>Welcome, {{ driver.name }}!</h1>
      <p class="status">
        Current Status: <span :class="statusClass">{{ driver.status }}</span>
      </p>
      <div class="status-buttons">
        <button
          class="status-button available"
          :disabled="driver.status === 'Available'"
          @click="updateStatus('Available')"
        >
          Available
        </button>
        <button
          class="status-button on-trip"
          :disabled="driver.status === 'On a Trip'"
          @click="updateStatus('On a Trip')"
        >
          On Trip
        </button>
        <button
          class="status-button offline"
          :disabled="driver.status === 'Offline'"
          @click="updateStatus('Offline')"
        >
          Offline
        </button>
      </div>
    </div>


    <!-- Metrics Section -->
    <div class="metrics">
      <div class="metric-box">
        <h3>{{ metrics[0].value }}</h3>
        <p>{{ metrics[0].label }}</p>
      </div>
      <div class="metric-box">
        <h3>{{ metrics[1].value }}</h3>
        <p>{{ metrics[1].label }}</p>
      </div>
      <div class="metric-box">
        <h3>{{ metrics[2].value }}</h3>
        <p>{{ metrics[2].label }}</p>
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
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      driver: null, // Driver details fetched from the server
      metrics: [], // Metrics fetched from the server
      upcomingTrip: null, // Upcoming trip fetched from the server
    };
  },
  computed: {
    statusClass() {
      // Dynamically assign classes based on driver status
      if (!this.driver) return '';
      return {
        available: this.driver.status === "Available",
        "on-trip": this.driver.status === "On a Trip",
        offline: this.driver.status === "Offline",
      };
    },
  },
  methods: {
    async fetchDashboardData() {
      try {
        // Fetch data from the API endpoint
        const response = await axios.get("https://16fd9f40-e2d5-46d3-883a-42b645f53d54.mock.pstmn.io/driver/dashboard");
        const data = response.data;

        // Update component data with the response
        this.driver = data.driver;
        this.metrics = [
          { label: "Trips completed", value: data.metrics.tripsCompleted },
          { label: "Earnings", value: `$${data.metrics.earnings}` },
          { label: "Average Rating", value: data.metrics.averageRating },
        ];
        this.upcomingTrip = data.upcomingTrip || null;
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    },
    updateStatus(newStatus) {
      if (this.driver) {
        this.driver.status = newStatus;
        console.log("Driver status updated to:", newStatus);
      }
    },
  },
  mounted() {
    this.fetchDashboardData(); // Fetch data when the component is mounted
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

/* Metrics Section */
.metrics {
  display: flex; /* Arrange boxes in a row */
  justify-content: space-between; /* Add space between boxes */
  gap: 20px; /* Space between each box */
  margin-bottom: 20px;
}

.metric-box {
  flex: 1; /* Allow boxes to take equal width */
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.metric-box h3 {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

.metric-box p {
  font-size: 16px;
  color: #555;
}

.metric-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
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

.status-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}

.status-button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
  transition: background-color 0.3s ease;
}

.status-button.available {
  background-color: green;
}

.status-button.on-trip {
  background-color: orange;
}

.status-button.offline {
  background-color: red;
}

.status-button:disabled {
  background-color: gray;
  cursor: not-allowed;
}
</style>
