<template>
  <div class="login-container">
    <h2>로그인</h2>
    <form @submit.prevent="login">
      <div>
        <label for="id">ID:</label>
        <input type="text" v-model="id" id="id" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">로그인</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      id: '',
      password: '',
      error: '',
      success: '',
    };
  },
  methods: {
    async login() {
      this.error = '';
      this.success = '';

      try {
        const response = await axios.post('https://example.com/api/login', {
          id: this.id,
          password: this.password,
        });

        if (response.data.success) {
          this.success = '로그인 성공!';
          // 토큰을 로컬스토리지에 저장
          localStorage.setItem('authToken', response.data.token);
        } else {
          this.error = '로그인 실패: ' + response.data.message;
        }
      } catch (error) {
        this.error = '서버 오류가 발생했습니다.';
        console.error(error);
      }
    },
  },
};
</script>

<style>
.login-container {
  max-width: 300px;
  margin: 0 auto;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.error {
  color: red;
}
.success {
  color: green;
}
</style>
