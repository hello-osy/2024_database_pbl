<!-- src/views/DriverProfiles.vue -->
<template>
  <div class="driver-profiles">
    <h2>Driver Profiles</h2>
    <p>Explore profiles of various drivers.</p>

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
      <img :src="driver.image" alt="Driver Image" class="profile-image" />
      <div class="profile-details">
        <h3 class="profile-name">{{ driver.name }}</h3>
        <p class="profile-bio">{{ driver.bio }}</p>
        <div class="profile-stats">
          <div class="stat-item">
            <span class="stat-value">{{ driver.rating }}</span>
            <span class="stat-label">Rating</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ driver.experience }} yrs</span>
            <span class="stat-label">Experience</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ driver.rides }}</span>
            <span class="stat-label">Rides</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DriverProfiles",
  data() {
    return {
      searchQuery: "", // 검색어
      drivers: [
        {
          id: 1,
          name: "John Doe",
          image: "https://via.placeholder.com/150",
          bio: "Experienced driver with over 5 years of expertise in the industry.",
          rating: 4.8,
          experience: 5,
          rides: 1200,
        },
        {
          id: 2,
          name: "Jane Smith",
          image: "https://via.placeholder.com/150",
          bio: "Professional and friendly driver with a passion for safe travel.",
          rating: 4.9,
          experience: 7,
          rides: 1500,
        },
        // 더 많은 드라이버 정보 추가 가능
      ],
    };
  },
  computed: {
    filteredDrivers() {
      return this.drivers.filter(driver =>
        driver.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
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

h2 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
}

p {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 30px;
}

.search-input {
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ddd;
  margin-bottom: 20px;
  width: 100%;
  max-width: 500px;
}

.profile-card {
  display: flex;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin: 15px;
  width: 100%;
  max-width: 500px;
  transition: transform 0.2s;
}

.profile-card:hover {
  transform: translateY(-5px);
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}

.profile-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.profile-name {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}

.profile-bio {
  font-size: 1rem;
  color: #666;
  margin: 10px 0;
}

.profile-stats {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 0.9rem;
  color: #888;
}
</style>
