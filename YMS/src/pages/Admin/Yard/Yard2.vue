<template>
  <div class="yard-content">
    <h2 class="yard-title">Yard: HOU_YARD_0002</h2>
    <!-- 검색 입력 필드 -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by Zone ID (e.g., T_ZONE_0001, C_ZONE_0002)"
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

    <!-- Custom Section for Yard Layout -->
    <div class="yard-layout">
      <!-- Display 4 sites in a 2x2 grid -->
      <div v-for="(site, index) in filteredSites" :key="index" class="site-box">
        <h3>{{ site.site_name }}</h3>
        <div class="site-info">
          <p>Storage Type: {{ site.storage_type }}</p>
          <p>Max Size: {{ site.y_max_size }}x{{ site.x_max_size }}</p>
        </div>

        <!-- Zone display under each site -->
        <div class="zone-grid">
          <div
            v-for="zone in site.zones"
            :key="zone.zone_id"
            class="zone-box"
            :class="zone.status.toLowerCase().replace(' ', '-')"
          >
            {{ zone.zone_id }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      searchQuery: "",
      statsCards: [
        { type: "warning", icon: "ti-server", title: "Total Zones", value: 50 },
        {
          type: "success",
          icon: "ti-wallet",
          title: "Available Zones",
          value: 30,
        },
        {
          type: "danger",
          icon: "ti-pulse",
          title: "Occupied Zones",
          value: 15,
        },
        {
          type: "info",
          icon: "ti-twitter-alt",
          title: "Inactive Zones",
          value: 5,
        },
      ],
      sites: [],
    };
  },
  methods: {
    async fetchYardData() {
      try {
        // Get sites data for HOU_YARD_0002
        const siteResponse = await axios.get(
          "http://localhost:8080/api/sites/by-yard/HOU_YARD_0002",
        );
        if (siteResponse.data.success) {
          const sites = siteResponse.data.data;

          // For each site, fetch its associated zone data
          for (const site of sites) {
            const zoneResponse = await axios.get(
              `http://localhost:8080/api/zones/by-site/${site.site_id}`,
            );
            site.zones = zoneResponse.data.success
              ? zoneResponse.data.data
              : [];
          }

          this.sites = sites;
        }
      } catch (error) {
        console.error("Error fetching yard data:", error.message);
      }
    },
  },
  computed: {
    filteredSites() {
      if (!this.searchQuery) {
        return this.sites;
      }

      return this.sites
        .map((site) => {
          const filteredZones = site.zones.filter((zone) =>
            zone.zone_id.toLowerCase().includes(this.searchQuery.toLowerCase()),
          );
          return filteredZones.length > 0
            ? { ...site, zones: filteredZones }
            : null;
        })
        .filter((site) => site !== null);
    },
  },
  mounted() {
    this.fetchYardData();
  },
};
</script>

<style scoped>
.yard-content {
  padding: 20px;
  background-color: #f4f4f9;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
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
  text-align: center;
}

.icon-container {
  font-size: 2rem;
  margin-right: 10px;
}

.zone-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
  margin-top: 15px;
}

.zone-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: bold;
  color: #333;
  text-align: center;
}

.zone-box.in-dock {
  background-color: #007bff;
  color: #fff;
}

.zone-box.in-parking {
  background-color: #28a745;
  color: #fff;
}

.zone-box.wrong-location {
  background-color: #dc3545;
  color: #fff;
}

.yard-layout {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 30px;
}

.site-box {
  padding: 20px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  display: flex;
  flex-direction: column;
}

.site-box h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.site-info {
  font-size: 1rem;
  margin-bottom: 15px;
}
</style>
