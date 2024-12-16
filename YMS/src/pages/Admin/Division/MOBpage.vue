<template>
    <div>
      <h1>MOB Yards</h1>
      <button @click="addYardToPage">Yard 추가</button>
      <button @click="updateYards">서버로 업데이트</button>
      <button @click="viewYards">데이터 확인</button> <!-- 데이터 확인 버튼 -->
  
      <ul v-if="yards.length">
        <li v-for="yard in yards" :key="yard.meta.yardId">
          <span>{{ yard.meta.yardName }}</span>
          <input
            v-model="yard.meta.yardName"
            placeholder="Yard 이름 수정"
          />
        </li>
      </ul>
      <p v-else>데이터가 없습니다.</p>
      <h2> Yard 링크 </h2>
      <ul>
        <li v-for="route in yards" :key="route.name">
          <router-link :to="route.path">{{ route.name }}</router-link>
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
        yards: [], // LA Yards 데이터를 저장
      };
    },
    methods: {
      addYardToPage() {
        addYard("MOB"); // LA에 Yard 추가
        this.updateYardsList(); // UI 업데이트
        console.log("this.yards: ", this.yards);
      },
      async updateYards() {
        await updateYardsToServer("LA"); // LA 데이터를 서버에 전송
      },
      updateYardsList() {
        this.yards = getMOBYardRoutes();
        console.log("yard 추가 후 경로: ", this.$router.options.routes);
      },
      viewYards() {
        console.log("현재 LA Yards 데이터:", this.yards);
        alert(`LA Yards 개수: ${this.yards.length}`);
      },
    },
    created() {
      this.updateYardsList(); // 컴포넌트 생성 시 LA 데이터를 로드
    },
    mounted() {
      this.updateYardsList();
    }
  };
  </script>