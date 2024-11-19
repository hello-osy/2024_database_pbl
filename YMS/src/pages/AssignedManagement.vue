<template>
  <div class="assigned-management">
    <h2>Assigned Equipment</h2>
    <table>
      <thead>
        <tr>
          <th>Equipment ID</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="equipment in assignedEquipments" :key="equipment.id">
          <td>{{ equipment.id }}</td>
          <td>{{ equipment.details || "No details" }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { EventBus } from "@/eventBus";

export default {
  data() {
    return {
      assignedEquipments: [], // 할당된 장비 리스트
    };
  },
  created() {
    // EventBus를 통해 데이터 수신
    EventBus.$on("update-assigned", this.updateAssignedEquipments);
  },
  beforeDestroy() {
    // 컴포넌트가 소멸되기 전에 EventBus 이벤트 해제
    EventBus.$off("update-assigned", this.updateAssignedEquipments);
  },
  methods: {
    updateAssignedEquipments(equipments) {
      this.assignedEquipments = equipments;
    },
  },
};
</script>

<style scoped>
.assigned-management {
  margin-top: 20px;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}
th {
  background-color: #f4f4f4;
}
</style>
