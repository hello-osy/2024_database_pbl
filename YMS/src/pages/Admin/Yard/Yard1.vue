<!-- src/views/Yard1.vue -->
<template>
  <div class="yard-content">
    <!-- 검색 입력 필드 -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by ID (e.g., T_001, C_002)"
      />
    </div>

    <!-- Stats Cards Section -->
    <div class="stats-row">
      <div class="stats-card" v-for="stats in statsCards" :key="stats.title">
        <div class="icon-container" :class="`icon-${stats.type}`">
          <i :class="stats.icon"></i>
        </div>
        <div class="stats-info">
          <p>{{ stats.title }}</p>
          <h3>{{ stats.value }}</h3>
        </div>
      </div>
    </div>

    <!-- Custom Section for Yard Layout (2x2) -->
    <div class="yard-layout">
      <div class="site" v-for="(site, index) in filteredSiteStatus" :key="index">
        <h3>{{ site.name }}</h3>
        <div class="truck-list">
          <div
            v-for="truck in site.trucks"
            :key="truck.id"
            class="truck-icon"
            :class="truck.status"
          >
            {{ truck.id }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    const generateTrucks = (prefix, count, status) => {
      return Array.from({ length: count }, (_, i) => ({
        id: `${prefix}_${String(i + 1).padStart(3, '0')}`, // 예: T_001, C_001
        status: status,
      }));
    };

    return {
      searchQuery: "", // 검색어 저장
      statsCards: [
        {
          type: "warning",
          icon: "ti-server",
          title: "Total Trucks",
          value: 40,
        },
        {
          type: "success",
          icon: "ti-wallet",
          title: "Total Chassis",
          value: 30,
        },
        {
          type: "danger",
          icon: "ti-pulse",
          title: "Total Containers",
          value: 30,
        },
        {
          type: "info",
          icon: "ti-twitter-alt",
          title: "Total Trailers",
          value: 10,
        },
      ],
      siteStatus: [
        {
          name: "Truck Site",
          trucks: generateTrucks("T", 40, "in-dock"),
        },
        {
          name: "Chassis Site",
          trucks: generateTrucks("C", 30, "in-parking"),
        },
        {
          name: "Container Site",
          trucks: generateTrucks("CT", 30, "in-dock"),
        },
        {
          name: "Trailer Site",
          trucks: generateTrucks("TL", 10, "in-parking"),
        },
      ],
    };
  },
  computed: {
    filteredSiteStatus() {
      if (!this.searchQuery) {
        return this.siteStatus;
      }
      
      // 검색어에 맞는 트럭만 필터링
      return this.siteStatus.map(site => {
        const filteredTrucks = site.trucks.filter(truck =>
          truck.id.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
        
        // 해당 사이트에 일치하는 트럭이 있을 경우만 반환
        return {
          ...site,
          trucks: filteredTrucks,
        };
      }).filter(site => site.trucks.length > 0);
    },
  },
};
</script>

<style scoped>
.yard-content {
  padding: 20px;
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
}

.stats-row {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  width: 100%;
}

.stats-card {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex: 1;
  min-width: 150px;
}

.icon-container {
  font-size: 2rem;
  margin-right: 15px;
}

.icon-warning {
  color: #ffc107;
}

.icon-success {
  color: #28a745;
}

.icon-danger {
  color: #dc3545;
}

.icon-info {
  color: #17a2b8;
}

.stats-info p {
  margin: 0;
  font-size: 0.9rem;
  color: #888;
}

.stats-info h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
}

.yard-layout {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
}

.site {
  padding: 15px;
  border-radius: 8px;
  background-color: #f8f9fa;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  min-width: 200px;
}

.site h3 {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #333;
}

.truck-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.truck-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: bold;
  color: #fff;
  text-align: center;
}

.in-dock {
  background-color: #007bff;
}

.in-parking {
  background-color: #28a745;
}

.wrong-location {
  background-color: #dc3545;
}
</style>
