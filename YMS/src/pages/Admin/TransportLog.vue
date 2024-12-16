<template>
  <div class="transport-log">
    <h2>Transport Log</h2>
    <p>Details of all transport activities are listed below.</p>

    <table class="log-table" v-if="transportLogs.length">
      <thead>
        <tr>
          <th @click="sortLogs('driver')">Driver <span v-if="sortBy === 'driver'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="sortLogs('vehicle')">Vehicle <span v-if="sortBy === 'vehicle'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="sortLogs('departZone')">Depart Zone <span v-if="sortBy === 'departZone'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="sortLogs('departDate')">Depart Date <span v-if="sortBy === 'departDate'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="sortLogs('arriveZone')">Arrive Zone <span v-if="sortBy === 'arriveZone'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="sortLogs('arriveDate')">Arrive Date <span v-if="sortBy === 'arriveDate'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="sortLogs('status')">Status <span v-if="sortBy === 'status'">{{ sortOrder === 'asc' ? '▲' : '▼' }}</span></th>
          <th style="width: 15%">Memo</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in transportLogs" :key="log.id">
          <td>{{ log.driver }}</td>
          <td>{{ log.vehicle }}</td>
          <td>{{ log.departZone }}</td>
          <td>{{ formatDate(log.departDate) }}</td>
          <td>{{ log.arriveZone }}</td>
          <td>{{ formatDate(log.arriveDate) }}</td>
          <td :class="getStatusClass(log.status)">{{ log.status }}</td>
          <td class="memo-cell" @click="showMemo(log.memo)">
            <span>{{ truncateMemo(log.memo) }}</span>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No transport logs available.</p>

    <!-- Memo Popup -->
    <div class="memo-popup" v-if="showPopup">
      <div class="popup-content">
        <h3>Memo Details</h3>
        <p>{{ selectedMemo }}</p>
        <button @click="closePopup">Close</button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";

export default {
  name: "TransportLog",
  data() {
    return {
      transportLogs: [], // 초기 데이터
      showPopup: false, // 팝업 표시 여부
      selectedMemo: "", // 선택된 메모 내용
      sortBy: "", // 현재 정렬 기준 필드
      sortOrder: "asc", // 정렬 순서 (asc: 오름차순, desc: 내림차순)
    };
  },
  methods: {
    async fetchTransportLogs() {
      try {
        const response = await axios.get(
          "http://localhost:8080/api/transport_logs/get_logs"
        );
        if (response.data.success) {
          this.transportLogs = response.data.data.map((log) => ({
            id: log.id,
            driver: log.driver,
            vehicle: log.vehicle,
            status: log.status,
            departDate: log.departDate ? new Date(log.departDate) : null, // null 체크 추가
            arriveDate: log.arriveDate ? new Date(log.arriveDate) : null, // null 체크 추가
            departZone: log.departZone || "N/A", // 기본값 설정
            arriveZone: log.arriveZone || "N/A", // 기본값 설정
            memo: log.memo || "No memo provided", // 기본값 설정
          }));
        } else {
          console.error(
            "Error fetching transport logs:",
            response.data.message
          );
        }
      } catch (error) {
        console.error("Error fetching transport logs:", error.message);
      }
    },
    formatDate(date) {
      return new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      }).format(date);
    },
    truncateMemo(memo) {
      // 메모 내용을 30자까지 축약하고 ... 추가
      return memo.length > 30 ? memo.substring(0, 30) + "..." : memo;
    },
    showMemo(memo) {
      // 메모를 팝업으로 표시
      this.selectedMemo = memo;
      this.showPopup = true;
    },
    closePopup() {
      this.showPopup = false;
      this.selectedMemo = "";
    },
    getStatusClass(status) {
      if (status === "Completed") return "Completed";
      if (status === "Delivering") return "Delivering";
      if (status === "Reserved") return "Reserved";
      if (status === "Rejected") return "Rejected";
      return "";
    },
    sortLogs(field) {
      if (this.sortBy === field) {
        // 같은 필드 클릭 시 정렬 순서 변경
        this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc";
      } else {
        // 새로운 필드 클릭 시 정렬 기준 변경
        this.sortBy = field;
        this.sortOrder = "asc";
      }
      this.transportLogs.sort((a, b) => {
        const valA = a[field] || ""; // null 값 방지
        const valB = b[field] || "";
        if (this.sortOrder === "asc") {
          return valA > valB ? 1 : valA < valB ? -1 : 0;
        } else {
          return valA < valB ? 1 : valA > valB ? -1 : 0;
        }
      });
    },
  },
  mounted() {
    this.fetchTransportLogs();
  },
};
</script>




<style scoped>
.transport-log {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 10px;
}

p {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 20px;
}

.log-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  margin-top: 20px;
  font-size: 1rem;
}

.log-table thead {
  background-color: #f1f1f1;
}

.log-table th,
.log-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
}

.log-table th {
  font-weight: bold;
  color: #333;
}

.log-table tr:hover {
  background-color: #f9f9f9;
}

.log-table .Rejected {
  color: #e63946;
}

.log-table .Completed {
  color: #38a169;
}

.log-table .Delivering {
  color: #f4a261;
}

.log-table .Reserved {
  color: #ba4cdb;
}

.memo-cell {
  cursor: pointer;
  color: #ABABAB;
  text-decoration: underline;
}

.memo-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border: 1px solid #ddd;
  padding: 20px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  width: 400px;
  text-align: center;
}

.popup-content h3 {
  margin-bottom: 15px;
}

.popup-content p {
  font-size: 1rem;
  margin-bottom: 20px;
}

.popup-content button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 4px;
}

.popup-content button:hover {
  background-color: #0056b3;
}
</style>
