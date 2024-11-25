<template>
    <div class="schedule-page">
      <!-- Header Section -->
      <div class="header">
        <h1>My Schedule</h1>
        <div class="view-toggle">
          <button :class="{ active: view === 'list' }" @click="view = 'list'">List View</button>
          <button :class="{ active: view === 'calendar' }" @click="view = 'calendar'">Calendar View</button>
        </div>
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
  
      <!-- Main Content -->
      <div class="content">
        <!-- List View -->
        <div v-if="view === 'list'" class="list-view">
          <ul>
            <li v-for="trip in filteredTrips" :key="trip.id">
              <h3>{{ trip.pickup }} → {{ trip.dropoff }}</h3>
              <p>Date: {{ trip.date }}</p>
              <p>Status: {{ trip.status }}</p>
              <button v-if="trip.status === 'upcoming'" @click="markCompleted(trip.id)">Mark as Completed</button>
            </li>
          </ul>
        </div>
  
        <!-- Calendar View -->
        <div v-if="view === 'calendar'" class="calendar-view">
          <calendar :events="trips" />
        </div>
      </div>
    </div>
</template>

<script>


export default {
  data() {
    return {
      view: "list", // Default view: list or calendar
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
      const trip = this.trips.find((t) => t.id === tripId);
      if (trip) {
        trip.status = "completed";
      }
    },
  },
};
</script>


<style scoped>
.schedule-page {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.view-toggle button {
  margin: 0 5px;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
}

.view-toggle button.active {
  background-color: #007bff;
  color: white;
}

.filters {
  margin: 15px 0;
}

.filters select {
  padding: 10px;
}

.list-view ul {
  list-style: none;
  padding: 0;
}

.list-view li {
  margin: 10px 0;
  padding: 10px;
  /* border: 1px solid #ddd; */
  border-radius: 5px;
}

/* Upcoming Trip */
.content {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.content h2 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
  font-family: 'Arial', sans-serif;
  text-transform: uppercase;
}

.content p {
  font-size: 16px;
  margin: 5px 0;
  line-height: 1.5;
  color: #555;
}

.content strong {
  color: #333;
}

.content:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.content div {
  padding: 10px 0;
}

/* Add animation to "No upcoming trips scheduled" */
.content p {
  animation: fadeIn 1s ease-in-out;
}
/* 
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
} */

</style>


