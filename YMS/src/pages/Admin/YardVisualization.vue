<template>
  <div class="parking-slot">
    <h1 class="title">Yard Visualization</h1>

    <!-- Status Cards Row -->
    <div class="stats-row">
      <div class="stats-card" v-for="(card, index) in statsCards" :key="index">
        <div class="stats-title">{{ card.title }}</div>
        <div class="stats-value">{{ card.value }}</div>
      </div>
    </div>

    <!-- First Line: Truck and Chassis -->
    <div class="line-container">
      <!-- Truck Slots -->
      <div class="section">
        <h2>Truck Area</h2>
        <div class="slots-container">
          <div v-for="(slot, index) in truckSlots" :key="index" class="slot">
            <img 
              v-if="slot.status === 'occupied'" 
              :src="truckImage" 
              :alt="`Truck ${slot.id}`"
              class="vehicle-image"
            />
            <div v-else class="empty-slot">Empty</div>
            <div class="slot-id">{{ slot.id }}</div>
          </div>
        </div>
      </div>

      <!-- Chassis Slots -->
      <div class="section">
        <h2>Chassis Area</h2>
        <div class="slots-container">
          <div v-for="(slot, index) in chassisSlots" :key="index" class="slot">
            <img 
              v-if="slot.status === 'occupied'" 
              :src="chassisImage" 
              :alt="`Chassis ${slot.id}`"
              class="vehicle-image"
            />
            <div v-else class="empty-slot">Empty</div>
            <div class="slot-id">{{ slot.id }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Second Line: Container and Trailer -->
    <div class="line-container">
      <!-- Container Slots -->
      <div class="section">
        <h2>Container Area</h2>
        <div class="slots-container">
          <div v-for="(slot, index) in containerSlots" :key="index" class="slot">
            <img 
              v-if="slot.status === 'occupied'" 
              :src="containerImage" 
              :alt="`Container ${slot.id}`"
              class="vehicle-image"
            />
            <div v-else class="empty-slot">Empty</div>
            <div class="slot-id">{{ slot.id }}</div>
          </div>
        </div>
      </div>

      <!-- Trailer Slots -->
      <div class="section">
        <h2>Trailer Area</h2>
        <div class="slots-container">
          <div v-for="(slot, index) in trailerSlots" :key="index" class="slot">
            <img 
              v-if="slot.status === 'occupied'" 
              :src="trailerImage" 
              :alt="`Trailer ${slot.id}`"
              class="vehicle-image"
            />
            <div v-else class="empty-slot">Empty</div>
            <div class="slot-id">{{ slot.id }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import truckImage from '@/assets/img/truck.png';
import chassisImage from '@/assets/img/chassis.png';
import containerImage from '@/assets/img/container.png';
import trailerImage from '@/assets/img/trailer.png';

export default {
  data() {
    return {
      truckImage,
      chassisImage,
      containerImage,
      trailerImage,
      statsCards: [
        { title: "Total Trucks", value: 10 },
        { title: "Total Chassis", value: 10 },
        { title: "Total Containers", value: 10 },
        { title: "Total Trailers", value: 10 },
      ],
      truckSlots: this.generateSlots('T', 10),
      chassisSlots: this.generateSlots('C', 10),
      containerSlots: this.generateSlots('CON', 10),
      trailerSlots: this.generateSlots('TR', 10),
    };
  },
  methods: {
    generateSlots(prefix, count) {
      return Array.from({ length: count }, (_, index) => ({
        id: `${prefix}-${String(index + 1).padStart(2, '0')}`,
        status: Math.random() > 0.5 ? 'occupied' : 'available',
      }));
    },
  },
};
</script>

<style scoped>
.parking-slot {
  padding: 20px;
  text-align: center;
  background-color: #f4f4f4;
}

.title {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
}

/* Status Cards */
.stats-row {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.stats-card {
  background-color: #ffffff;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 265px;
}

.stats-title {
  font-size: 1rem;
  color: #555;
}

.stats-value {
  font-size: 1.5rem;
  font-weight: bold;
  margin-top: 5px;
}

/* Parking Layout */
.line-container {
  display: flex;
  gap: 20px;
  margin: 10px;
  justify-content: center;
}

.section {
  background-color: #fff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.section h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.slots-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: center;
}

.slot {
  width: 100px;
  height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.vehicle-image {
  max-width: 50px;
  margin-bottom: 5px;
}

.empty-slot {
  font-size: 14px;
  color: #bbb;
  font-weight: bold;
}

.slot-id {
  font-size: 12px;
  color: #444;
  font-weight: bold;
}
</style>
