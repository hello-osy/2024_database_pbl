<template>
  <div class="assigned-management">
    <h2>Assigned Equipment</h2>
    <table>
      <thead>
        <tr>
          <th>Log ID</th>
          <th>Depart Zone</th>
          <th>Arrive Zone</th>
          <th>Driver ID</th>
          <th>Depart Date</th>
          <th>Arrive Date</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in transportLogs" :key="log.id">
          <td>{{ log.id }}</td>
          <td>{{ log.depart_zone }}</td>
          <td>{{ log.arrive_zone }}</td>
          <td>{{ log.driver_id }}</td>
          <td>{{ log.depart_date || 'N/A' }}</td>
          <td>{{ log.arrive_date || 'N/A' }}</td>
          <td>
            <button @click="releaseLog(log.id)">Release</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AssignedManagement",
  data() {
    return {
      transportLogs: [], // 할당된 장비 로그
    };
  },
  methods: {
    async fetchTransportLogs() {
      try {
        const { data } = await axios.get("http://localhost:8080/api/transport_logs/assigned");
        if (data.success) {
          this.transportLogs = data.data.map(log => ({
            id: log.id,
            depart_zone: log.depart_zone || "N/A",
            arrive_zone: log.arrive_zone || "N/A",
            driver_id: log.driver_id || "Unassigned",
            depart_date: log.depart_date || "N/A",
            arrive_date: log.arrive_date || "N/A",
          }));
        } else {
          console.error("Failed to fetch data:", data.message);
        }
      } catch (error) {
        console.error("Error fetching transport logs:", error.message);
      }
    },

    async releaseLog(logId) {
      try {
        console.log(`Releasing log ID: ${logId}`);

        // 1. 운송 로그 할당 해제
        const releaseResponse = await axios.post(
          `http://localhost:8080/api/transport_logs/release/${logId}`
        );

        if (releaseResponse.data.success) {
          // 2. 해당 로그 제거
          this.transportLogs = this.transportLogs.filter(log => log.id !== logId);
          alert("Log released successfully and equipment status updated.");
        } else {
          console.error("Failed to release log:", releaseResponse.data.message);
        }
      } catch (error) {
        console.error("Error during release:", error.response?.data || error.message);
      }
    },
  },
  mounted() {
    this.fetchTransportLogs(); // 페이지 로드시 로그 데이터 가져오기
  },
};
</script>

<style scoped>
.assigned-management {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  font-size: 1.5rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

table th {
  background-color: #f4f4f4;
}

button {
  padding: 5px 10px;
  background-color: #ff6b6b;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #ff5252;
}
</style>
