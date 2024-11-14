<template>
  <div id="app">
    <header>
      <h1>Vue 로그인 예제</h1>
    </header>
    <main>
      <LoginExample />
    </main>
  </div>
</template>

<script>
import LoginExample from './components/LoginExample.vue';

export default {
  components: {
    LoginExample,
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

header {
  background-color: #42b983;
  color: white;
  padding: 10px 0;
}

header h1 {
  margin: 0;
}

main {
  padding: 20px;
}
</style>
