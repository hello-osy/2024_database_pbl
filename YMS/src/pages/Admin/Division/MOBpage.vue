<template>
  <div class="yard-container">
    <h1>MOB Yards</h1>
    <button @click="addYardToPage" class="btn">Yard 추가</button>
    <button @click="updateYards" class="btn btn-update">서버로 업데이트</button>
    <button @click="viewYards" class="btn btn-view">데이터 확인</button>

    <ul v-if="yards.length" class="yard-list">
      <li v-for="yard in yards" :key="yard.meta.yardId" class="yard-item">
        <span class="yard-name">{{ yard.meta.yardName }}</span>
        <input
          v-model="yard.meta.yardName"
          placeholder="Yard 이름 수정"
          class="yard-input"
        />
      </li>
    </ul>
    <p v-else class="no-data">데이터가 없습니다.</p>

    <h2>Yard Link</h2>
    <ul class="link-list">
      <li v-for="route in yards" :key="route.name" class="link-item">
        <router-link :to="route.path" class="yard-link">{{ route.name }}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import { getYardData, addYard, updateYardsToServer } from "@/router";
import { getMOBYardRoutes } from '../../../router';

export default {
  data() {
    return {
      yards: [], // MOB Yards 데이터를 저장
    };
  },
  methods: {
    addYardToPage() {
      addYard("MOB");
      this.updateYardsList();
      console.log("this.yards: ", this.yards);
    },
    async updateYards() {
      await updateYardsToServer("MOB"); // Fixed: Changed "LA" to "MOB"
    },
    updateYardsList() {
      this.yards = getMOBYardRoutes();
      console.log("yard 추가 후 경로: ", this.$router.options.routes);
    },
    viewYards() {
      console.log("현재 MOB Yards 데이터:", this.yards); // Fixed: Changed LA to MOB
      alert(`MOB Yards 개수: ${this.yards.length}`); // Fixed: Changed LA to MOB
    },
  },
  created() {
    this.updateYardsList();
  },
  mounted() {
    this.updateYardsList();
  }
};
</script>

<style scoped>
.yard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1, h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-weight: 600;
  position: relative;
}

h1::after, h2::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60px;
  height: 4px;
  background: #007bff;
  border-radius: 2px;
}

.btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.25rem;
  margin: 0.5rem;
  cursor: pointer;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.btn-update {
  background-color: #28a745;
}

.btn-view {
  background-color: #17a2b8;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.btn:active {
  transform: translateY(0);
}

.yard-list, .link-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
}

.yard-item, .link-item {
  display: flex;
  align-items: center;
  margin: 1rem 0;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.yard-item:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.yard-name {
  margin-right: 1rem;
  font-weight: 600;
  color: #2c3e50;
  min-width: 120px;
}

.yard-input {
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 6px;
  flex: 1;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.yard-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.yard-link {
  text-decoration: none;
  color: #007bff;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.yard-link:hover {
  background-color: rgba(0, 123, 255, 0.1);
  text-decoration: none;
  transform: translateX(5px);
}

.no-data {
  color: #6c757d;
  font-style: italic;
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  border: 2px dashed #dee2e6;
}

@media (max-width: 768px) {
  .yard-container {
    padding: 1rem;
  }
  
  .yard-item {
    flex-direction: column;
    align-items: stretch;
  }
  
  .yard-name {
    margin-bottom: 0.5rem;
  }
  
  .btn {
    width: 100%;
    margin: 0.5rem 0;
  }
}
</style>