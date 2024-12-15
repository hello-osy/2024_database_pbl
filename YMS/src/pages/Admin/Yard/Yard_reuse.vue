<template>
  <!-- <<<<<<< HEAD -->
    <div class="yard-content">
      <div class="search-bar">
        <input v-model="searchQuery" type="text" placeholder="Search by ID (e.g., T_001, C_002)" />
      </div>
  
      <div class="stats-row">
        <div class="stats-card" v-for="stats in statsCards" :key="stats.title">
          <div class="stats-content">
            <div class="stats-title">{{ stats.title }}</div>
            <div class="stats-value">{{ stats.value }}</div>
          </div>
        </div>
      </div>
  
      <div class="yard-layout">
        <div class="site-block" v-for="(site, index) in filteredSiteStatus" :key="index">
          <h3 class="site-title">{{ site.name }}</h3>
          <div class="truck-list">
            <div
              v-for="truck in site.trucks"
              :key="truck.id"
              :class="['truck-icon', truck.status, { assigned: isAssigned(truck) }]"
              @click="selectTruck(truck)"
            >
              {{ truck.id }}
            </div>
          </div>
        </div>
      </div>
  
      <!-- Truck만 선택 가능한 Modal -->
      <div v-if="selectedTruck && (selectedTruck.id.startsWith('T'))" class="modal">
        <div class="modal-content">
          <h3>
            Configure {{ selectedTruck.id.startsWith('TL') ? 'Trailer' : 'Truck' }} {{ selectedTruck.id }}
          </h3>
          
          <div v-if="selectedTruck && !selectedTruck.id.startsWith('TL')">
          
          <div class="modal-grid">
          <!-- Left Column -->
            <div class="modal-column">
              <label>Choose Chassis:</label>
              <select v-model="selectedChassis">
                <option v-for="chassis in chassisList" :key="chassis.id" :value="chassis">
                  {{ chassis.id }}
                </option>
              </select>

              <label>Choose Container:</label>
              <select v-model="selectedContainer">
                <option v-for="container in containerList" :key="container.id" :value="container">
                  {{ container.id }}
                </option>
              </select>

              <label>Choose Trailer:</label>
              <select v-model="selectedTrailer">
                <option v-for="trailer in trailerList" :key="trailer.id" :value="trailer">
                  {{ trailer.id }}
                </option>
              </select>
            </div>

            <!-- Right Column -->
            <div class="modal-column">
              <label>Arrival Date:</label>
              <input v-model="arriveDate" type="date" placeholder="Select arrival date" />

              <label>Arrive Zone:</label>
              <input v-model="arriveZone" placeholder="Enter arrival zone" />

              <label>Assign Driver:</label>
              <select v-model="selectedDriver">
                <option v-for="driver in drivers" :key="driver.User_ID" :value="driver">
                  {{ driver.User_ID }}
                </option>
              </select>
            </div>
          </div>

          <button @click="confirmSelection">Confirm</button>
          <button @click="cancelSelection">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions } from "vuex";
  import axios from "axios";

  export default {
    data() {
      return {
        searchQuery: "",
        selectedTruck: null,
        selectedChassis: null,
        selectedContainer: null,
        selectedTrailer: null, // 추가된 데이터
        departZone: "",
        arriveZone: "",
        arriveDate: "", // 추가된 데이터
        selectedDriver: null,
        statsCards: [],
        siteStatus: [],
        drivers: [],
      };
    },
    computed: {
      filteredSiteStatus() {
        if (!this.searchQuery) {
          return this.siteStatus;
        }
  
        return this.siteStatus
          .map((site) => {
            const filteredTrucks = site.trucks.filter((truck) =>
              truck.id.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
            return { ...site, trucks: filteredTrucks };
          })
          .filter((site) => site.trucks.length > 0);
      },
      chassisList() {
        return this.siteStatus.find((site) => site.name === "Chassis Site").trucks;
      },
      containerList() {
        return this.siteStatus.find((site) => site.name === "Container Site").trucks;
      },
      trailerList() {
        return this.siteStatus.find((site) => site.name === "Trailer Site").trucks;
      },
    },
    methods: {
      extractYardIdFromUrl() {
        const fullPath = this.$route.fullPath; // 현재 URL 경로
        const yardId = fullPath.split("/").pop(); // 마지막 경로 추출 (예: HOU_YARD_0002)
        this.yardId = yardId;
        console.log("Extracted Yard ID:", this.yardId);
      },
      async fetchYardStats(){
        try {
          const response = await axios.get("http://localhost:8080/api/yard/stats", {
            params: { yard_id: this.yardId },
          });

          if (response.data.success) {
            const { total_trucks, total_chassis, total_containers, total_trailers } =
              response.data.data;

            this.statsCards = [
              { type: "warning", title: "Total Trucks", value: total_trucks },
              { type: "success", title: "Total Chassis", value: total_chassis },
              { type: "danger", title: "Total Containers", value: total_containers },
              { type: "info", title: "Total Trailers", value: total_trailers },
            ];
          } else {
            console.error("Failed to fetch yard stats:", response.data.message);
          }
        } catch (error) {
          console.error("Error fetching yard stats:", error.message);
        }
      },

      async fetchDriverStats() {
        try {
          const response = await axios.get("http://localhost:8080/api/driver/stats", {
            params: { yard_id: this.yardId },
          });

          if (response.data.success) {
            this.drivers = response.data.data;
            console.log("Driver stats fetched successfully:", this.drivers);
          } else {
            console.error("Failed to fetch driver stats:", response.data.message);
          }
        } catch (error) {
          console.error("Error fetching driver stats:", error.message);
        }
      },
      
      async fetchSiteStats() {
        try {
          const response = await axios.get("http://localhost:8080/api/yard/siteStatus", {
            params: { yard_id: this.yardId },
          });

          if (response.data.success) {
            // JSON 데이터를 siteStatus 포맷으로 변환
            this.siteStatus = response.data.data.map((site) => ({
              name: site.name,
              trucks: [
                ...site.equipments.Truck.map((truck) => ({
                  id: truck.id,
                  status: truck.status,
                })),
                ...site.equipments.Chassis.map((chassis) => ({
                  id: chassis.id,
                  status: chassis.status,
                })),
                ...site.equipments.Container.map((container) => ({
                  id: container.id,
                  status: container.status,
                })),
                ...site.equipments.Trailer.map((trailer) => ({
                  id: trailer.id,
                  status: trailer.status,
                })),
              ],
            }));
            console.log("Updated siteStatus:", this.siteStatus);
          } else {
            console.error("Failed to fetch site status:", response.data.message);
          }
        } catch (error) {
          console.error("Error fetching site status:", error.message);
        }
      },



      ...mapActions(["addEquipment"]), // Vuex의 addEquipment 액션 매핑
      selectTruck(truck) {
        // Truck(T) 또는 Trailer(TL)만 선택 가능
        if (truck.id.startsWith("T") || truck.id.startsWith("TL")) {
          this.selectedTruck = truck;
          this.selectedChassis = null;
          this.selectedContainer = null;
        } else {
          alert("Only Truck can be configured.");
        }
      },
      isAssigned(equipment) {
        return this.$store.state.assignedEquipments.some(
          (assigned) => assigned.id === equipment.id
        );
      },


      confirmSelection() {
        // 검증 로직
        if (!this.selectedTruck) {
          alert("Please select a truck.");
          return;
        }
        if (!this.selectedChassis && !this.selectedTrailer) {
          alert("Please select chassis or trailer for the truck.");
          return;
        }
        if ((this.selectedChassis && !this.selectedContainer) && !this.selectedTrailer) {
          alert("Please select a container.");
          return;
        }
        if (this.selectedChassis && this.selectedContainer && this.selectedTrailer){
          alert("Can't Choose Chassis and Trailer both")
          this.selectedChassis = null;
          this.selectedContainer = null;
          this.selectedTrailer = null;
          return;
        }
        if (!this.arriveDate){
          alert("Pleas select a arrival date");
          return;
        }
        if (!this.arriveZone.trim()) {
          alert("Please enter an arrival zone.");
          return;
        }
        if (!this.selectedDriver) {
          alert("Please assign a driver.");
          return;
        }

        // 입력값이 모두 유효한 경우
        const newAssignments = [this.selectedTruck, this.selectedChassis, this.selectedContainer]
          .filter(Boolean)
          .map((equipment) => ({
            id: equipment.id,
            details: {
              departZone: this.departZone || "N/A",
              arriveZone: this.arriveZone || "N/A",
              driver: this.selectedDriver?.User_ID || "Unassigned",
            },
          }));

        // Vuex에 데이터 추가
        newAssignments.forEach((equipment) => {
          this.addEquipment(equipment);
        });

        // 입력값 초기화
        this.resetSelection();
      },


      cancelSelection() {
        this.resetSelection();
      },
      resetSelection() {
        this.selectedTruck = null;
        this.selectedChassis = null;
        this.selectedContainer = null;
        this.selectedTrailer =  null;
        this.arriveDate = null;
        this.departZone = "";
        this.arriveZone = "";
        this.selectedDriver = null;
      },
    },
    // URL 변경 감지
    watch: {
      $route(to, from) {
        console.log("Route changed:", from.fullPath, "to:", to.fullPath);
        this.extractYardIdFromUrl(); // URL에서 Yard ID 다시 추출
        this.fetchYardStats(); // 새 데이터를 다시 요청
        this.fetchDriverStats();
        this.fetchSiteStats();
      },
    },
    mounted(){
      this.extractYardIdFromUrl();
      this.fetchYardStats();
      this.fetchDriverStats();
      this.fetchSiteStats();
    }
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
  justify-content: space-between;
}

.stats-card {
  flex: 1;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  color: #000000;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.stats-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stats-title {
  font-size: 1.2rem;
  margin-bottom: 10px;
  font-weight: bold;
}

.stats-value {
  font-size: 2rem;
  font-weight: bold;
}

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

.in-dock {
  background-color: #007bff;
}
.Available {
  background-color: #28a745;
}
.Reserved{
  border: 2px solid #ffa726;
  box-shadow: 0 0 8px #ffa726;
}


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
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px 30px;
  border-radius: 15px;
  width: 60%;
  max-width: 90%;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.modal-content h3 {
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #333;
}

.modal-content label {
  display: block;
  margin: 10px 0 5px;
  font-size: 1rem;
  color: #555;
}

.modal-content select,
.modal-content input {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.modal-content button {
  margin: 10px 5px;
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.modal-content button:first-child {
  background-color: #28a745;
  color: white;
}

.modal-content button:first-child:hover {
  background-color: #218838;
}

.modal-content button:last-child {
  background-color: #dc3545;
  color: white;
}

.modal-content button:last-child:hover {
  background-color: #c82333;
}

.modal-grid {
  display: flex;
  gap: 20px;
}

.modal-column {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.modal-column label {
  margin-top: 10px;
}

.modal-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

.modal-buttons button {
  flex: 1;
  margin: 0 10px;
}

</style>

