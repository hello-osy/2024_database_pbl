<template>
  <div class="transport-log">
    <h2>Transport Log</h2>
    <p>Details of all transport activities are listed below.</p>

    <!-- 로그 테이블 -->
    <table class="log-table">
      <thead>
        <tr>
          <th>Date</th>
          <th>Driver</th>
          <th>Vehicle</th>
          <th>Status</th>
          <th>Distance (km)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in transportLogs" :key="log.id">
          <td>{{ log.date }}</td>
          <td>{{ log.driver }}</td>
          <td>{{ log.vehicle }}</td>
          <td :class="log.status.toLowerCase()">{{ log.status }}</td>
          <td>{{ log.distance }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TransportLog",
  data() {
    return {
      transportLogs: [], // 초기 데이터
    };
  },
  methods: {
    async fetchTransportLogs() {
      try {
        const response = await axios.get(
          "http://localhost:8080/api/transport_logs",
        );
        if (response.data.success) {
          this.transportLogs = response.data.data;
        } else {
          console.error(
            "Error fetching transport logs:",
            response.data.message,
          );
        }
      } catch (error) {
        console.error("Error fetching transport logs:", error.message);
      }
    },
  },
  mounted() {
    // 컴포넌트가 마운트될 때 데이터 가져오기
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

/* 로그 테이블 스타일 */
.log-table {
  width: 100%;
  max-width: 800px;
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

.log-table .completed {
  color: #28a745; /* 초록색 (완료) */
}

.log-table .in-progress {
  color: #ffc107; /* 노란색 (진행 중) */
}

.log-table .scheduled {
  color: #007bff; /* 파란색 (예정) */
}
</style>
