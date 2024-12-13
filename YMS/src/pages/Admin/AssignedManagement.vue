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
          <th>Assigned</th>
          <th>Depart Date</th>
          <th>Arrive Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in transportLogs" :key="log.id">
          <td>{{ log.id }}</td>
          <td>{{ log.depart_zone }}</td>
          <td>{{ log.arrive_zone }}</td>
          <td>{{ log.driver_id }}</td>
          <td>{{ log.depart_date }}</td>
          <td>{{ log.arrive_date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<!-- <script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(["assignedEquipments"]), // Vuex에서 데이터를 가져옴
  },
};
</script> -->


<script>
import axios from "axios";

export default {
  name: "AssignedManagement",
  data() {
    return {
      transportLogs: [], // API에서 가져올 데이터를 저장
    };
  },
  methods: {
    async fetchTransportLogs() {
      try {
        const response = await axios.get("http://localhost:8080/api/transport_logs/assigned");
        if (response.data.success) {
          this.transportLogs = response.data.data;
        } else {
          console.error("데이터 가져오기 실패:", response.data.message);
        }
      } catch (error) {
        console.error("에러 발생:", error.message);
      }
    },
  },
  mounted() {
    // 컴포넌트가 로드될 때 API 호출
    this.fetchTransportLogs();
  },
};
</script>



<style scoped>
.assigned-management {
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}

h2 {
  margin-bottom: 20px;
}
</style>
