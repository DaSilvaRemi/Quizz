<template>
  <h1 class="text-center">Home page</h1>
  <ScoreListManager />
  <div class="text-center">
    <RouterLink to="/new-quiz" class="btn btn-primary">Démarrer le quiz !</RouterLink>
  </div>
</template>

<script>
import ScoreListManager from "@/components/ScoreListManager.vue";

export default {
  name: "HomePage",
  components: {
    ScoreListManager
  },
};
</script>