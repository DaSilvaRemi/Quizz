<template>
  <AppHeader />
  <RouterView />
</template>

<script>
import { RouterView } from 'vue-router';
import AppHeader from './components/AppHeader.vue';

export default {
  name: "App",
  components: {
    AppHeader
  },
}
</script>

<style scoped></style>
