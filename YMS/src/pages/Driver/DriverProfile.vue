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
          style="display: none"
        />
      </div>
      <h1>{{ driver.user_id }}</h1>
      <p>Click on the picture for change profile-picture</p>
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
        <li>
          <strong>Private Truck Info:</strong> {{ driver.privateTruckInfo }}
        </li>
        <li><strong>Trips Completed:</strong> {{ driver.tripsCompleted }}</li>
        <li><strong>Monthly Earnings:</strong> {{ driver.monthlyEarnings }}</li>
        <li><strong>Average Ratings:</strong> {{ driver.averageRatings }}</li>
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
        user_id: "",
        name: "",
        picture: require("@/assets/img/driver-profile03.png"), // Load asset image using require
        phone: "",
        email: "",
        address: "",
        vehicle: "Not assigned",
        privateTruckInfo: "",
        tripsCompleted: 0,
        monthlyEarnings: 0,
        averageRatings: 0,
      },
    };
  },
  methods: {
    async fetchDriverInfo() {
      try {
        const token = localStorage.getItem("token");
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

        if (response.status === 200) {
          const data = await response.json();
          if (data.success) {
            const driverInfo = data.driver;
            this.driver = {
              ...this.driver,
              user_id: driverInfo.user_id,
              name: driverInfo.name || "",
              phone: driverInfo.phone || "Not provided",
              email: driverInfo.email || "Not provided",
              address: driverInfo.address || "Not provided",
              truck_id: driverInfo.truck_id || "Not assigned",
              privateTruckInfo: driverInfo.truck_info || "Not assigned",
              tripsCompleted: driverInfo.tripsCompleted || 0,
              monthlyEarnings: driverInfo.monthlyEarnings
                ? `$${parseFloat(driverInfo.monthlyEarnings).toFixed(2)}`
                : "$0.00",
              averageRatings: driverInfo.averageRatings
                ? `parseFloat(driverInfo.averageRatings).toFixed(2)`
                : "0.00",
            };

            // Transport_Log에서 Assigned == 1인 truck_id 가져오기
            await this.fetchAssignedVehicle(
              driverInfo.user_id,
              driverInfo.truck_id,
            );
          } else {
            console.error("Failed to fetch driver info:", data.message);
          }
        } else {
          console.error(
            "Failed to fetch driver info. Status:",
            response.status,
          );
        }
      } catch (error) {
        console.error("An error occurred while fetching driver info:", error);
      }
    },
    async fetchAssignedVehicle(userId) {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          `http://localhost:8080/api/transport_logs/all`,
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
          console.log("API Response Data:", data); // 전체 데이터 출력

          if (data.success) {
            // userId와 Assigned가 1인 데이터를 찾음
            const assignedLog = data.data.find(
              (log) => log.Driver_ID === userId && log.Assigned === 1,
            );

            console.log("Assigned Log:", assignedLog); // 필터링된 로그 출력

            // Truck_ID 값 설정
            if (assignedLog && assignedLog.Truck_ID) {
              this.driver.vehicle = `${assignedLog.Truck_ID}`;
            } else {
              this.driver.vehicle = "Not assigned";
            }
          } else {
            console.error("Failed to fetch transport logs:", data.message);
            this.driver.vehicle = "Not assigned"; // 기본값 설정
          }
        } else {
          console.error(
            "Failed to fetch transport logs. Status:",
            response.status,
          );
        }
      } catch (error) {
        console.error(
          "An error occurred while fetching assigned vehicle:",
          error,
        );
        this.driver.vehicle = "Not assigned"; // 예외 발생 시 기본값 설정
      }
    },
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
  mounted() {
    this.fetchDriverInfo(); // Fetch driver info when the component is mounted
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
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
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
  background-color: #4caf50;
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
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  cursor: pointer;
}

.info-section h2 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #333;
  text-align: center;
  font-family: "Arial", sans-serif;
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
