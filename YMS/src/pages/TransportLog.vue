<!-- src/views/TransportLog.vue -->
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
export default {
  name: "TransportLog",
  data() {
    return {
      transportLogs: [
        {
          id: 1,
          date: "2024-11-12",
          driver: "John Doe",
          vehicle: "Truck 23",
          status: "Completed",
          distance: 150,
        },
        {
          id: 2,
          date: "2024-11-11",
          driver: "Jane Smith",
          vehicle: "Van 45",
          status: "In Progress",
          distance: 75,
        },
        {
          id: 3,
          date: "2024-11-10",
          driver: "Alice Johnson",
          vehicle: "Truck 34",
          status: "Delayed",
          distance: 120,
        },
        // 더 많은 데이터 추가 가능
      ],
    };
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

.log-table .delayed {
  color: #dc3545; /* 빨간색 (지연) */
}
</style>
