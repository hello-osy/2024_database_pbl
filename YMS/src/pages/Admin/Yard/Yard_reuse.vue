<template>
    <div>
      <h2>Yard Details: {{ yardId }}</h2>
      <p>Details about the yard will be displayed here.</p>
    </div>
</template>
  
  <script>
  export default {
    name: "Yard",
    props: {
      yardId: {
        type: String,
        required: true,
      },
    },
    mounted() {
      console.log("Yard ID:", this.yardId); // 전달된 yardId 확인
      // 여기서 yardId로 API 요청을 통해 추가 데이터를 가져올 수 있음
    },
  };
  </script>
  
  <style scoped>
  /* 필요한 스타일 추가 */
  </style>