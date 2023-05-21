<template>
  <AppHeader />
  <RouterView />
</template>

<script>
/**
 * name: "App"
 * 
 * Description: The root component of the application.
 * 
 * Components:
 * - AppHeader: Component for displaying the application header.
 * - RouterView: Component for rendering the current route component.
 * 
 * Data:
 * - None
 * 
 * Lifecycle hooks:
 * - None
 * 
 * Methods:
 * - None
 */
import { RouterView } from 'vue-router';
import AppHeader from './components/AppHeader.vue';

export default {
  name: "App",
  components: {
    AppHeader,
  },
}
</script>

<style scoped></style>
