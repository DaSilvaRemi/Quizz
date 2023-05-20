<template>
  <h1 class="text-center">Accueil</h1>
  <ScoreListManager />
  <div class="text-center">
    <RouterLink to="/new-quiz" class="btn btn-primary">Démarrer le quiz !</RouterLink>
  </div>
</template>

<script>
/**
 * Component: HomePage
 * Description: Represents the home page of the application.
 *
 * Components:
 *   - ScoreListManager: The component for managing and displaying the list of scores.
 *
 * No data or methods defined in this component.
 */
 import { RouterLink } from 'vue-router';
import ScoreListManager from "@/components/ScoreListManager.vue";

export default {
  name: "HomePage",
  components: {
    ScoreListManager
  },
};
</script>