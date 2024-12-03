<template>
  <div class="assigned-management">
    <h2>Assigned Equipment</h2>
    <table>
      <thead>
        <tr>
          <th>Equipment ID</th>
          <th>Depart Yard</th>
          <th>Arrive Division</th>
          <th>Driver</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="equipment in assignedEquipments" :key="equipment.id">
          <td>{{ equipment.id }}</td>
          <td>{{ equipment.details.departZone }}</td>
          <td>{{ equipment.details.arriveZone }}</td>
          <td>{{ equipment.details.driver }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(["assignedEquipments"]), // Vuex에서 데이터를 가져옴
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
