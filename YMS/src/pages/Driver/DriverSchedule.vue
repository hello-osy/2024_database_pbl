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
        <option value="in_progress">In Progress</option>
        <option value="completed">Completed</option>
      </select>
    </div>

    <!-- Main Content -->
    <div class="content">
      <!-- Filtered Trips -->
      <div class="schedule-section" v-if="filteredTrips.length">
        <div class="trip" v-for="trip in filteredTrips" :key="trip.id">
          <h3>{{ trip.departZone }} → {{ trip.arriveZone }}</h3>
          <p><strong>Depart Date:</strong> {{ trip.departDate }}</p>
          <p><strong>Arrive Date:</strong> {{ trip.arriveDate }}</p>
          <div v-if="trip.assigned === 0" class="action-buttons">
            <button @click="acceptTrip(trip.id)">Accept</button>
            <button @click="declineTrip(trip.id)">Decline</button>
          </div>
          <div v-else-if="trip.assigned === 1" class="action-buttons">
            <button @click="markCompleted(trip.id)">Mark as Completed</button>
          </div>
          <div v-else-if="trip.assigned === 2" class="action-buttons">
            <button disabled>Completed</button>
          </div>
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
      trips: [],
    };
  },
  computed: {
    filteredTrips() {
      if (!this.trips) {
        return []; // `trips`가 정의되지 않았을 경우 빈 배열 반환
      }
      // 필터 조건에 따라 분류
      return this.trips.filter((trip) => {
        if (this.filterStatus === "all") return true; // 모든 상태
        if (this.filterStatus === "upcoming") return trip.assigned === 0; // upcoming
        if (this.filterStatus === "in_progress") return trip.assigned === 1; // in progress
        if (this.filterStatus === "completed") return trip.assigned === 2; // completed
        return false; // 기본 값
      });
    },
  },
  methods: {
    async fetchTrips() {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          "http://localhost:8080/api/transport_logs/get_logs_by_driver",
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (response.ok) {
          const data = await response.json();
          console.log("Fetched trips:", data);
          if (data.success) {
            this.trips = data.data.map((trip) => ({
              ...trip,
              assigned: Number(trip.assigned), // 명시적으로 숫자로 변환
            }));
            console.log("Trips after conversion:", this.trips); // 변환된 데이터 확인
          } else {
            console.error("Failed to fetch trips:", data.message);
          }
        } else {
          console.error("API request failed. Status:", response.status);
        }
      } catch (error) {
        console.error("An error occurred while fetching trips:", error);
      }
    },
    markCompleted(logId) {
      const tripIndex = this.trips.findIndex((t) => t.id === logId);
      if (tripIndex !== -1) {
        this.updateTripStatus(logId, true, true) // 서버에서 상태 업데이트
          .then(() => {
            this.trips[tripIndex].assigned = 2; // 새로운 상태값 설정
            console.log(`Trip ${logId} marked as completed.`);
          })
          .catch((error) => {
            console.error(`Failed to mark trip ${logId} as completed:`, error);
          });
      }
    },
    acceptTrip(logId) {
      const tripIndex = this.trips.findIndex((t) => t.id === logId);
      if (tripIndex !== -1) {
        this.trips[tripIndex].assigned = true;
        this.trips[tripIndex].status = "upcoming"; // 상태 필드 업데이트
        this.updateTripStatus(logId, true);
      }
    },
    declineTrip(logId) {
      const tripIndex = this.trips.findIndex((t) => t.id === logId);
      if (tripIndex !== -1) {
        this.trips.splice(tripIndex, 1); // 로컬에서 즉시 제거
        this.updateTripStatus(logId, -1); // 거부된 상태를 서버에 전달
      }
    },
    async updateTripStatus(logId, assigned, completed = false) {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          `http://localhost:8080/api/update-transport-log`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ log_id: logId, assigned, completed }),
          },
        );
        if (!response.ok) {
          throw new Error(`API request failed with status ${response.status}`);
        }
        return response.json(); // 성공 시 JSON 반환
      } catch (error) {
        console.error("An error occurred while updating trip status:", error);
        throw error; // 에러를 호출부로 전달
      }
    },
  },
  mounted() {
    this.fetchTrips();
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
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
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
