<template>
  <div class="driver-profiles">
    <h2>Driver Profiles</h2>
    <p>Explore profiles of various drivers from the database.</p>

    <!-- 검색 입력 -->
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search by driver name"
      class="search-input"
    />

    <!-- 검색 결과가 없을 때 메시지 -->
    <p v-if="filteredDrivers.length === 0">No drivers found.</p>

    <!-- 프로필 카드 -->
    <div
      class="profile-card"
      v-for="driver in filteredDrivers"
      :key="driver.id"
    >
      <div class="profile-details">
        <h3 class="profile-name">{{ driver.name }}</h3>
        <p class="profile-location">Location: {{ driver.current_location }}</p>
        <p class="profile-status">Status: {{ driver.current_status }}</p>
        <p class="profile-truck-info">
          Private Truck: {{ driver.private_truck_info }}
        </p>
        <p class="profile-truck-id">Truck ID: {{ driver.truck_id }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DriverProfiles",
  data() {
    return {
      searchQuery: "", // 검색어
      drivers: [], // 드라이버 데이터를 담을 배열
    };
  },
  computed: {
    filteredDrivers() {
      return this.drivers.filter((driver) =>
        driver.name.toLowerCase().includes(this.searchQuery.toLowerCase()),
      );
    },
  },
  methods: {
    async fetchDrivers() {
      try {
        const response = await axios.get("http://localhost:8080/api/drivers");
        if (response.data.success) {
          this.drivers = response.data.data;
        } else {
          console.error("Error fetching drivers:", response.data.message);
        }
      } catch (error) {
        console.error("Error fetching drivers:", error.message);
      }
    },
  },
  mounted() {
    // 컴포넌트 마운트 시 데이터 로드
    this.fetchDrivers();
  },
};
</script>

<style scoped>
.driver-profiles {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-card {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  margin: 10px 0;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-details {
  text-align: left;
}

.profile-name {
  font-size: 1.5rem;
  color: #333;
}

.profile-location,
.profile-status,
.profile-truck-info,
.profile-truck-id {
  font-size: 1rem;
  color: #555;
  margin: 5px 0;
}
</style>
