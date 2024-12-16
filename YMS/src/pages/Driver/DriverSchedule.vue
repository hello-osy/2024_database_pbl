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
            <button
              :disabled="
                assigningTrip || hasInProgressTrip || trip.assigned !== 0
              "
              @click.once="handleAcceptWithLogUpdate(trip.id)"
            >
              Accept
            </button>
            <button @click="declineTripWithLogUpdate(trip.id)">Decline</button>
          </div>
          <div v-else-if="trip.assigned === 1" class="action-buttons">
            <button @click="markAsCompleted(trip.id)">Mark as Completed</button>
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
      <!-- Log Memo Popup -->
      <div v-if="showPopup" class="popup-overlay">
        <div class="popup">
          <h3>Log Memo</h3>
          <textarea
            v-model="logMemo"
            placeholder="Enter memo here..."
          ></textarea>
          <div class="popup-actions">
            <button @click="submitMemo">Submit</button>
            <button @click="closePopup">Cancel</button>
          </div>
        </div>
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
      assigningTrip: false, // 현재 할당 중인지 추적
      showPopup: false, // 팝업 상태
      logMemo: "", // 작성된 메모
      currentTripId: null, // 현재 작업 중인 trip ID
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
    hasInProgressTrip() {
      // 진행 중인 작업이 있는지 확인
      return this.trips.some((trip) => trip.assigned === 1);
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
          if (data.success) {
            this.trips = data.data.map((trip) => ({
              ...trip,
              assigned: Number(trip.assigned), // 명시적으로 숫자로 변환
            }));
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
    async updateTransportLogStatus(logId, action) {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          "http://localhost:8080/api/transport_log/update_status",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ log_id: logId, action }),
          },
        );

        const result = await response.json();
        if (!response.ok) {
          alert(
            "Failed to update transport log status: " +
              (result.message || "Unknown error"),
          );
          throw new Error(
            result.message || "Failed to update transport log status",
          );
        }
        return result;
      } catch (error) {
        console.error("Error updating transport log status:", error);
        throw error;
      }
    },
    async handleAccept(logId) {
      if (this.hasInProgressTrip) {
        alert(
          "You already have an assigned trip in progress. You cannot accept a new trip until the current one is completed.",
        );
        return;
      }
      try {
        await this.updateTransportLogStatus(logId, "accept");
        await this.fetchTrips();
        alert("Trip accepted successfully!");
      } catch (error) {
        console.error("Error while accepting trip:", error);
      }
    },
    async handleReject(logId) {
      try {
        await this.updateTransportLogStatus(logId, "reject");
        await this.fetchTrips();
        alert("Trip declined successfully!");
      } catch (error) {
        console.error("Error while rejecting trip:", error);
      }
    },
    async handleComplete() {
      if (!this.logMemo.trim()) {
        alert("Memo cannot be empty.");
        return;
      }
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          "http://localhost:8080/api/transport_logs/update_memo",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              log_id: this.currentTripId,
              log_memo: this.logMemo,
              assigned: 2,
            }),
          },
        );

        const result = await response.json();
        if (response.ok && result.success) {
          await this.fetchTrips();
          alert("Trip marked as completed!");
          this.closePopup();
          this.currentTripId = null; // 현재 Trip ID 초기화
          this.logMemo = ""; // 메모 초기화
        } else {
          throw new Error(result.message || "Failed to complete trip");
        }
      } catch (error) {
        console.error("Error completing trip:", error);
        alert("Failed to mark trip as completed.");
      }
    },
    openMemoPopup(tripId) {
      this.showPopup = true;
      this.currentTripId = tripId;
      const trip = this.trips.find((t) => t.id === tripId);
      this.logMemo = trip?.logMemo || ""; // 기존 메모 로드
    },
    closePopup() {
      this.showPopup = false;
      this.currentTripId = null;
      this.logMemo = "";
    },
    async submitMemo() {
      try {
        if (!this.logMemo.trim()) {
          alert("Memo cannot be empty.");
          return;
        }
        const response = await this.updateTripLogMemo(
          this.currentTripId,
          this.logMemo,
          2,
        );
        if (response.success) {
          const tripIndex = this.trips.findIndex(
            (trip) => trip.id === this.currentTripId,
          );
          if (tripIndex !== -1) {
            this.trips[tripIndex].assigned = 2; // assigned 값을 변경
            this.trips[tripIndex].logMemo = this.logMemo; // 메모 업데이트
          }
          alert("Memo updated and trip marked as completed.");
          this.closePopup();
        } else {
          alert("Failed to update memo: " + response.message);
        }
      } catch (error) {
        alert("An error occurred while updating memo.");
        console.error("Error in submitMemo:", error);
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
        console.log("서버 응답 상태:", response.status);
        const result = await response.json();
        console.log("서버 응답 데이터:", result);

        return result;
      } catch (error) {
        console.error("Error updating trip status:", error);
        throw error; // 에러를 호출부로 전달
      }
    },
    async updateTripLogMemo(logId, logMemo, assigned) {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          `http://localhost:8080/api/transport_logs/update_memo`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              log_id: logId,
              log_memo: logMemo,
              assigned: assigned,
            }),
          },
        );

        const result = await response.json();
        console.log("API response:", result);

        if (!response.ok) {
          throw new Error(result.message || "Failed to update log memo");
        }
        return result;
      } catch (error) {
        console.error("Error updating trip log memo:", error);
        throw error;
      }
    },
  },
  mounted() {
    this.fetchTrips();
    console.log("현재 trips 상태:", this.trips);
    console.log("현재 assigningTrip 상태:", this.assigningTrip);
    console.log("hasInProgressTrip 상태:", this.hasInProgressTrip);
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

/* Disabled Button */
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
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

/* Popup Styles */
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.popup textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.popup textarea:focus {
  outline: none;
  border-color: #007bff;
}

.popup-actions {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.popup-actions button {
  flex: 1;
}
</style>
