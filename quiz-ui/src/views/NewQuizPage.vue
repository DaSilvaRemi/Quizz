<template>
  <div class="d-flex flex-column align-items-center pt-5">
    <form id="new-quiz-form" @submit.prevent="launchNewQuiz">
      <h2 class="text-center">Commencer un nouveau quiz</h2>
      <div class="form-outline mb-4">
        <label class="form-label" for="nom-joueur">Saisissez votre nom : </label>
        <input class="form-control" type="text" id="nom-joueur" name="nom-joueur" placeholder="Votre nom"
          aria-describedby="Le nom qui sera affiché sur la table des scores" v-model="username" required>
      </div>
      <div class="text-center">
        <button type="submit" class="btn btn-primary btn-block mb-4">Commencer !</button>
      </div>
    </form>
  </div>
</template>

<script>
/**
 * Component: NewQuizPage
 * Description: Represents the page for starting a new quiz.
 *
 * Data:
 *   - username (String): The username of the player.
 *
 * Methods:
 *   - created(): Lifecycle hook called when the component is created. Retrieves the player name from storage.
 *   - launchNewQuiz(): Launches a new quiz by clearing storage, saving the player name, and navigating to the questions page.
 */
import participationStorageService from "@/services/ParticipationStorageService.js";

export default {
  name: "NewQuizPage",
  data() {
    return {
      username: ''
    };
  },
  created(){
    this.username = participationStorageService.getPlayerName() ?? '';
  },
  methods: {
    /**
     * Launches a new quiz by clearing storage, saving the player name, and navigating to the questions page.
     */
    launchNewQuiz() {
      if(!this.username){
        return;
      }

      participationStorageService.clear();
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    }
  }
};
</script>
