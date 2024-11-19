<!-- src/views/TransportLog.vue -->
<template>
  <div class="transport-log">
    <h2>Transport Log</h2>
    <p>View transport log details below:</p>

    <!-- Transport Log Table -->
    <table class="log-table">
      <thead>
        <tr>
          <th>Log ID</th>
          <th>Driver ID</th>
          <th>Container ID</th>
          <th>Chassis ID</th>
          <th>Truck ID</th>
          <th>Trailer ID</th>
          <th>Depart Zone</th>
          <th>Depart Date</th>
          <th>Arrive Zone</th>
          <th>Arrive Date</th>
          <th>Log Memo</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in logs" :key="log.Log_ID">
          <td>{{ log.Log_ID }}</td>
          <td>{{ log.Driver_ID }}</td>
          <td>{{ log.Container_ID }}</td>
          <td>{{ log.Chassis_ID }}</td>
          <td>{{ log.Truck_ID }}</td>
          <td>{{ log.Trailer_ID }}</td>
          <td>{{ log.Depart_Zone_ID }}</td>
          <td>{{ log.Depart_Date }}</td>
          <td>{{ log.Arrive_Zone_ID }}</td>
          <td>{{ log.Arrive_Date }}</td>
          <td>{{ log.Log_memo }}</td>
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
      logs: [
        {
          Log_ID: "L001",
          Driver_ID: "D001",
          Container_ID: "C001",
          Chassis_ID: "CH001",
          Truck_ID: "T001",
          Trailer_ID: "TR001",
          Depart_Zone_ID: "Z001",
          Depart_Date: "2024-01-01 08:00",
          Arrive_Zone_ID: "Z002",
          Arrive_Date: "2024-01-01 12:00",
          Log_memo: "Delivered on time",
        },
        {
          Log_ID: "L002",
          Driver_ID: "D002",
          Container_ID: "C002",
          Chassis_ID: "CH002",
          Truck_ID: "T002",
          Trailer_ID: "TR002",
          Depart_Zone_ID: "Z003",
          Depart_Date: "2024-01-02 09:30",
          Arrive_Zone_ID: "Z004",
          Arrive_Date: "2024-01-02 15:00",
          Log_memo: "Delayed due to traffic",
        },
        // 추가 로그 데이터를 여기에 계속 추가할 수 있습니다.
      ],
    };
  },
};
</script>

<style scoped>
.transport-log {
  padding: 20px;
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
}

.log-table th,
.log-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.log-table th {
  background-color: #f8f9fa;
  color: #333;
  font-weight: bold;
}

.log-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.log-table tr:hover {
  background-color: #e9ecef;
}
</style>
