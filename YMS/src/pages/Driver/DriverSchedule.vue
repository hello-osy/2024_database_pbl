<template>
  <div class="schedule-page">
    <!-- Header Section -->
    <div class="header">
      <h1>My Schedule</h1>
    </div>

    <!-- Filters Section -->
    <div class="filters">
      <select v-model="filterStatus">
        <option value="all">All</option>
        <option value="upcoming">Upcoming</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
      </select>
    </div>

      <!-- New Trips -->
      <div class="schedule-section" v-if="newTrips.length">
        <h2>New Trips</h2>
        <div class="trip" v-for="trip in newTrips" :key="trip.id">
          <h3>{{ trip.pickup }} → {{ trip.dropoff }}</h3>
          <p><strong>Date:</strong> {{ trip.date }}</p>
          <p><strong>Time:</strong> {{ trip.time }}</p>
          <div class="action-buttons">
            <button class="accept-button" @click="acceptTrip(trip.id)">Accept</button>
            <button class="decline-button" @click="declineTrip(trip.id)">Decline</button>
          </div>
        </div>
      </div>

      <!-- Main Content -->
    <div class="content">
      <!-- Filtered Trips -->
      <div class="schedule-section" v-if="filteredTrips.length">
        <div class="trip" v-for="trip in filteredTrips" :key="trip.id">
          <h3>{{ trip.pickup }} → {{ trip.dropoff }}</h3>
          <p><strong>Date:</strong> {{ trip.date }}</p>
          <p><strong>Time:</strong> {{ trip.time }}</p>
          <div v-if="trip.status === 'upcoming'" class="action-buttons">
            <button @click="markCompleted(trip.id)">Mark as Completed</button>
          </div>
          <p v-else-if="trip.status === 'completed'" class="status-label completed">Completed</p>
          <p v-else-if="trip.status === 'cancelled'" class="status-label cancelled">Cancelled</p>
        </div>
      </div>

      <!-- No Trips Message -->
      <div v-else class="no-trips">
        <p>No trips to show.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filterStatus: "all", // Default filter
      trips: [
        { 
          id: 1,
          pickup: "Location A",
          dropoff: "Location B",
          date: "2024-11-22",
          time: "10:00 AM",
          status: "upcoming",
        },
        {
          id: 2,
          pickup: "Location C",
          dropoff: "Location D",
          date: "2024-11-23",
          time: "2:00 PM",
          status: "completed",
        },
        {
          id: 3,
          pickup: "Location E",
          dropoff: "Location F",
          date: "2024-11-24",
          time: "11:00 AM",
          status: "cancelled",
        },
      ],
      newTrips: [
        {
          id: 4,
          pickup: "Location G",
          dropoff: "Location H",
          date: "2024-11-25",
          time: "9:00 AM",
        },
      ], // Store new trips assigned by the manager
    };
  },
  computed: {
    filteredTrips() {
      if (this.filterStatus === "all") {
        return this.trips;
      }
      return this.trips.filter((trip) => trip.status === this.filterStatus);
    },
  },
  methods: {
    markCompleted(tripId) {
      // Find the trip and update its status
      const tripIndex = this.trips.findIndex((t) => t.id === tripId);
      if (tripIndex !== -1) {
        const updatedTrip = { ...this.trips[tripIndex], status: "completed" };
        this.trips.splice(tripIndex, 1, updatedTrip); // Replace with updated trip
        alert(`Trip has been marked as completed.`);
      } else {
        alert(`Error: Trip not found.`);
      }
    },
    acceptTrip(tripId) {
      const tripIndex = this.newTrips.findIndex((t) => t.id === tripId);
      if (tripIndex !== -1) {
        const trip = this.newTrips.splice(tripIndex, 1)[0];
        trip.status = "upcoming";
        this.trips.push(trip);
      }
    },
    declineTrip(tripId) {
      this.newTrips = this.newTrips.filter((t) => t.id !== tripId);
    },
  },
};
</script>

<style scoped>
/* General Styles */
.schedule-page {
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f7f7f7;
  min-height: 100vh;
}

.header {
  text-align: left;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 24px;
  color: #333;
}

/* Filters Section */
.filters {
  margin-bottom: 20px;
  text-align: left;
}

.filters select {
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  font-size: 14px;
  background-color: #fff;
  width: 200px;
  transition: border-color 0.3s ease;
}

.filters select:focus {
  border-color: #007bff;
  outline: none;
}

/* Schedule Section */
.schedule-section {
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.schedule-section h2 {
  margin-bottom: 15px;
  font-size: 18px;
  color: #333;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}

.trip {
  padding: 10px 0;
  border-bottom: 1px solid #ddd;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.trip:last-child {
  border-bottom: none;
}

.trip h3 {
  font-size: 16px;
  color: #007bff;
  margin-bottom: 5px;
}

.trip p {
  margin: 3px 0;
  font-size: 14px;
  color: #555;
}

/* No Trips Message */
.no-trips {
  text-align: center;
  color: #999;
  font-size: 16px;
  margin-top: 20px;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 12px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  color: white;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
  transform: translateY(-2px);
}

/* Accept Button */
button {
  background-color: #4caf50;
}

button:hover {
  background-color: #45a049;
}

/* Decline Button */
button.decline-button {
  background-color: #f44336;
}

button.decline-button:hover {
  background-color: #e53935;
}

/* Completed and Cancelled Status Labels */
.status-label {
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 12px;
  color: white;
  display: inline-block;
}

.status-label.completed {
  background-color: #4caf50;
}

.status-label.cancelled {
  background-color: #f44336;
}
</style>