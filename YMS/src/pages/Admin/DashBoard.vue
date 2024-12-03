<template>
  <div class="division-page">
    <h2 class="page-title">Division</h2>
    <p class="page-description">Select a Yard to view its location on the map.</p>

    <!-- Yard 리스트 -->
    <div class="yard-container">
      <div
        class="yard-card"
        v-for="yard in yards"
        :key="yard.name"
        @click="selectYard(yard)"
        :class="{ 'active-yard': selectedYard && selectedYard.name === yard.name }"
      >
        <h3 class="yard-title">{{ yard.name }}</h3>
        <p class="yard-coordinates">
          Latitude: {{ yard.lat.toFixed(4) }}, Longitude: {{ yard.lng.toFixed(4) }}
        </p>
      </div>
    </div>

    <!-- 지도 표시 영역 -->
    <div id="map" class="map"></div>
  </div>
</template>

<script>
export default {
  name: "Division",
  data() {
    return {
      map: null,
      marker: null,
      yards: [
        { name: "Yard 1", lat: 37.7749, lng: -122.4194 }, // 샘플 좌표 (샌프란시스코)
        { name: "Yard 2", lat: 34.0522, lng: -118.2437 }, // 샘플 좌표 (로스앤젤레스)
        { name: "Yard 3", lat: 40.7128, lng: -74.006 }, // 샘플 좌표 (뉴욕)
      ],
      selectedYard: null,
    };
  },
  mounted() {
    // Google Maps API 스크립트 로드
    if (!window.google) {
      const script = document.createElement("script");
      script.src = `https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap`;
      script.async = true;
      window.initMap = this.initMap;
      document.head.appendChild(script);
    } else {
      this.initMap();
    }
  },
  methods: {
    initMap() {
      // 기본 지도 설정 (처음엔 첫 번째 Yard 위치로 설정)
      this.map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: this.yards[0].lat, lng: this.yards[0].lng },
        zoom: 8,
      });

      // 첫 번째 Yard에 마커 설정
      this.selectedYard = this.yards[0];
      this.updateMarker();
    },
    selectYard(yard) {
      this.selectedYard = yard;
      this.map.setCenter({ lat: yard.lat, lng: yard.lng });
      this.updateMarker();
    },
    updateMarker() {
      // 기존 마커 제거
      if (this.marker) {
        this.marker.setMap(null);
      }

      // 새로운 마커 추가
      this.marker = new google.maps.Marker({
        position: { lat: this.selectedYard.lat, lng: this.selectedYard.lng },
        map: this.map,
        title: this.selectedYard.name,
      });
    },
  },
};
</script>

<style scoped>
.division-page {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-title {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 10px;
}

.page-description {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 20px;
  text-align: center;
}

.yard-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.yard-card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px 20px;
  width: 250px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.yard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.active-yard {
  border-color: #007bff;
  box-shadow: 0 6px 12px rgba(0, 123, 255, 0.4);
}

.yard-title {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #007bff;
}

.yard-coordinates {
  font-size: 0.9rem;
  color: #555;
}

.map {
  width: 100%;
  max-width: 800px;
  height: 500px;
  background-color: #e0e0e0;
  margin-top: 30px;
  border-radius: 10px;
}
</style>
