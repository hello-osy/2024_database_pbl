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
  
      <!-- Truck 또는 Trailer만 선택 가능한 Modal -->
      <div v-if="selectedTruck && (selectedTruck.id.startsWith('T') || selectedTruck.id.startsWith('TL'))" class="modal">
        <div class="modal-content">
          <h3>
            Configure {{ selectedTruck.id.startsWith('TL') ? 'Trailer' : 'Truck' }} {{ selectedTruck.id }}
          </h3>
  
          <div v-if="selectedTruck && !selectedTruck.id.startsWith('TL')">
            <label>Choose Chassis:</label>
            <select v-model="selectedChassis">
              <option v-for="chassis in chassisList" :key="chassis.id" :value="chassis">
                {{ chassis.id }}
              </option>
            </select>
          </div>
  
          <label>Choose Container:</label>
          <select v-model="selectedContainer">
            <option v-for="container in containerList" :key="container.id" :value="container">
              {{ container.id }}
            </option>
          </select>
  
          <label>Depart Zone:</label>
          <input v-model="departZone" placeholder="Enter departure zone" />
  
          <label>Arrive Zone:</label>
          <input v-model="arriveZone" placeholder="Enter arrival zone" />
  
          <label>Assign Driver:</label>
          <select v-model="selectedDriver">
            <option v-for="driver in drivers" :key="driver.User_ID" :value="driver">
              {{ driver.User_ID }}
            </option>
          </select>
  
          <button @click="confirmSelection">Confirm</button>
          <button @click="cancelSelection">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { mapActions } from "vuex";
  
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
        statsCards: [],
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
    },
    methods: {
      extractYardIdFromUrl() {
        const fullPath = this.$route.fullPath; // 현재 URL 경로
        const yardId = fullPath.split("/").pop(); // 마지막 경로 추출 (예: HOU_YARD_0002)
        this.yardId = yardId;
        console.log("Extracted Yard ID:", this.yardId);
      },

      async fetchYardStats() {
        try {
          const response = await axios.get("http://localhost:5000/api/yard/stats", {
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
      
      ...mapActions(["addEquipment"]), // Vuex의 addEquipment 액션 매핑
      selectTruck(truck) {
        // Truck(T) 또는 Trailer(TL)만 선택 가능
        if (truck.id.startsWith("T") || truck.id.startsWith("TL")) {
          this.selectedTruck = truck;
          this.selectedChassis = null;
          this.selectedContainer = null;
        } else {
          alert("Only Trucks and Trailers can be configured.");
        }
      },
      isAssigned(equipment) {
        return this.$store.state.assignedEquipments.some(
          (assigned) => assigned.id === equipment.id
        );
      },
      confirmSelection() {
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
    mounted(){
      this.extractYardIdFromUrl();
      this.fetchYardStats();
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
  .in-parking {
    background-color: #28a745;
  }
  .assigned {
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
    width: 400px;
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
  </style>
  <!-- =======
    <Yard :yardId="'HOU_YARD_0001'" />
  </template>
  
  <script>
  import Yard from "@/pages/Admin/Yard/Yard.vue";
  
  export default {
    components: {
      Yard,
    },
  };
  </script>
  >>>>>>> develop -->
  