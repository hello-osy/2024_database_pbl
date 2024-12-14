<template>
  <div class="dashboard">
    <!-- Header Section -->
    <div class="header">
      <h1>{{ welcomeMessage }}</h1>
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
export default {
  data() {
    return {
      driver: {
        user_id: "", // User ID를 저장할 필드 추가
        name: "", // Driver의 이름 (Name이 없을 경우 User_ID로 대체)
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
    welcomeMessage() {
      // Welcome 메시지 동적으로 생성
      return `Welcome, ${this.driver.name || this.driver.user_id}!`;
    },
  },
  methods: {
    async fetchDriverInfo() {
      try {
        const token = localStorage.getItem("token");
        console.log("Token being sent:", token); // 디버깅용
        if (!token) {
          console.error("Token is missing. Please log in again.");
          return;
        }

        const response = await fetch("http://localhost:8080/api/driver-info", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        console.log("Response status:", response.status); // 응답 상태 코드 확인
        const data = await response.json();
        if (data.success) {
          this.driver.user_id = data.driver.user_id; // User_ID 설정
          this.driver.name = data.driver.name || ""; // Name 설정 (없을 경우 빈 값)
          this.driver.status = data.driver.status; // Status 설정
          console.log("Driver info fetched successfully:", data);
        } else {
          console.error("Failed to fetch driver info:", data.message);
        }
      } catch (error) {
        console.error("An error occurred while fetching driver info:", error);
      }
    },
    async updateStatus(newStatus) {
      if (this.driver.status === newStatus) {
        console.log(`Status is already ${newStatus}, no update needed.`);
        return;
      }
      try {
        const token = localStorage.getItem("token");
        console.log("Token being sent for status update:", token); // 디버깅용
        if (!token) {
          console.error("Token is missing. Please log in again.");
          return;
        }

        const response = await fetch(
          "http://localhost:8080/api/update-status",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ status: newStatus }),
          },
        );

        console.log("Response status for status update:", response.status); // 응답 상태 코드 확인
        const data = await response.json();
        if (data.success) {
          this.driver.status = newStatus; // 상태 업데이트
          console.log("Driver status updated successfully:", data);
        } else {
          console.error("Failed to update driver status:", data.message);
        }
      } catch (error) {
        console.error("An error occurred while updating driver status:", error);
      }
    },
    /*
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
    updateStatus(newStatus) {
      this.driver.status = newStatus;
      console.log("Driver status updated to:", newStatus);
    },
    */
  },
  mounted() {
    this.fetchDriverInfo();
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
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
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
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.upcoming-trip h2 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
  font-family: "Arial", sans-serif;
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
