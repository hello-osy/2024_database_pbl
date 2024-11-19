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

    <!-- Custom Section for Yard Layout -->
    <div class="yard-layout">
      <div class="site-block" v-for="(site, index) in filteredSiteStatus" :key="index">
        <h3 class="site-title">{{ site.name }}</h3>
        <div class="truck-list">
          <div
            v-for="truck in site.trucks"
            :key="truck.id"
            :class="['truck-icon', truck.status, { 'assigned': isAssigned(truck) }]"
            @click="selectTruck(truck)"
          >
            {{ truck.id }}
          </div>
        </div>
      </div>
    </div>

    <!-- Truck 결합 선택 모달 -->
    <div v-if="selectedTruck" class="modal">
      <div class="modal-content">
        <h3>Configure {{ selectedTruck.id.startsWith('TL') ? 'Trailer' : 'Truck' }} {{ selectedTruck.id }}</h3>

        <!-- Truck 선택 시 Chassis 및 Container 선택 가능 -->
        <div v-if="selectedTruck && !selectedTruck.id.startsWith('TL')">
          <label>Choose Chassis:</label>
          <select v-model="selectedChassis">
            <option v-for="chassis in chassisList" :key="chassis.id" :value="chassis">
              {{ chassis.id }}
            </option>
          </select>
        </div>

        <!-- Trailer 선택 시 Container만 선택 가능 -->
        <label>Choose Container:</label>
        <select v-model="selectedContainer">
          <option v-for="container in containerList" :key="container.id" :value="container">
            {{ container.id }}
          </option>
        </select>

        <!-- 출발지와 목적지 입력 -->
        <label>Depart Zone:</label>
        <input v-model="departZone" placeholder="Enter departure zone" />

        <label>Arrive Zone:</label>
        <input v-model="arriveZone" placeholder="Enter arrival zone" />

        <!-- 드라이버 할당 -->
        <label>Assign Driver:</label>
        <select v-model="selectedDriver">
          <option v-for="driver in drivers" :key="driver.User_ID" :value="driver">
            {{ driver.User_ID }}
          </option>
        </select>

        <!-- 확인 및 취소 버튼 -->
        <button @click="confirmSelection">Confirm</button>
        <button @click="cancelSelection">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import { EventBus } from "@/eventBus";

export default {
  data() {
    const generateTrucks = (prefix, count, status) => {
      return Array.from({ length: count }, (_, i) => ({
        id: `${prefix}_${String(i + 1).padStart(3, "0")}`,
        status: status,
      }));
    };

    return {
      searchQuery: "",
      selectedTruck: null,
      selectedChassis: null,
      selectedContainer: null,
      departZone: "",
      arriveZone: "",
      selectedDriver: null,
      statsCards: [
        { type: "warning", icon: "ti-server", title: "Total Trucks", value: 40 },
        { type: "success", icon: "ti-wallet", title: "Total Chassis", value: 30 },
        { type: "danger", icon: "ti-pulse", title: "Total Containers", value: 30 },
        { type: "info", icon: "ti-twitter-alt", title: "Total Trailers", value: 10 },
      ],
      siteStatus: [
        { name: "Truck Site", trucks: generateTrucks("T", 40, "in-dock") },
        { name: "Chassis Site", trucks: generateTrucks("C", 30, "in-parking") },
        { name: "Container Site", trucks: generateTrucks("CT", 30, "in-dock") },
        { name: "Trailer Site", trucks: generateTrucks("TL", 10, "in-parking") },
      ],
      drivers: [
        { User_ID: "D001", Current_Location: "Zone A", Current_Status: "Active" },
        { User_ID: "D002", Current_Location: "Zone B", Current_Status: "Inactive" },
        { User_ID: "D003", Current_Location: "Zone C", Current_Status: "On Break" },
      ],
      assignedEquipments: [], // 할당된 장비 목록
    };
  },
  computed: {
    filteredSiteStatus() {
      if (!this.searchQuery) {
        return this.siteStatus;
      }

      return this.siteStatus
        .map(site => {
          const filteredTrucks = site.trucks.filter(truck =>
            truck.id.toLowerCase().includes(this.searchQuery.toLowerCase())
          );
          return { ...site, trucks: filteredTrucks };
        })
        .filter(site => site.trucks.length > 0);
    },
    chassisList() {
      return this.siteStatus.find(site => site.name === "Chassis Site").trucks;
    },
    containerList() {
      return this.siteStatus.find(site => site.name === "Container Site").trucks;
    },
  },
  methods: {
    selectTruck(truck) {
      this.selectedTruck = truck;
      this.selectedChassis = null;
      this.selectedContainer = null;
    },
    isAssigned(equipment) {
      return this.assignedEquipments.some(assigned => assigned.id === equipment.id);
    },
    confirmSelection() {
      const newAssignments = [this.selectedTruck, this.selectedChassis, this.selectedContainer]
        .filter(Boolean)
        .map(equipment => ({
          id: equipment.id,
          details: {
            departZone: this.departZone || "N/A",
            arriveZone: this.arriveZone || "N/A",
            driver: this.selectedDriver?.User_ID || "Unassigned",
          },
        }));

      newAssignments.forEach(assignment => {
        if (!this.assignedEquipments.some(existing => existing.id === assignment.id)) {
          this.assignedEquipments.push(assignment);
        }
      });

      // Emit to AssignedManagement via EventBus
      console.log("Emitting to EventBus:", this.assignedEquipments); // 디버깅용 로그
      EventBus.$emit("update-assigned", this.assignedEquipments);

      this.resetSelection();
    },
    cancelSelection() {
      this.resetSelection();
    },
    resetSelection() {
      this.selectedTruck = null;
      this.selectedChassis = null;
      this.selectedContainer = null;
      this.departZone = "";
      this.arriveZone = "";
      this.selectedDriver = null;
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

/* Site 블록 스타일 */
.yard-layout {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
}

.site-block {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.site-title {
  font-size: 1.3rem;
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

.in-dock { background-color: #007bff; }
.in-parking { background-color: #28a745; }
.assigned { border: 2px solid #ffa726; box-shadow: 0 0 8px #ffa726; } /* 할당된 장비 시각적 구분 */

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
}
</style>