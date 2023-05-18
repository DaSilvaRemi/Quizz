<template>
  <div class="d-flex flex-column align-items-center pt-5">
    <form @submit.prevent="submit">
      <h2 class="text-center">Commencer un nouveau quiz</h2>
      <div class="form-outline mb-4">
        <label class="form-label" for="nom-joueur">Saisissez votre nom : </label>
        <input class="form-control" type="text" id="nom-joueur" name="nom-joueur" placeholder="Votre nom"
          aria-describedby="Le nom qui sera affiché sur la table des scores" v-model="username" required>
      </div>
      <div class="text-center">
        <button type="submit" class="btn btn-primary btn-block mb-4" @click="launchNewQuiz">Commencer !</button>
      </div>
    </form>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService.js";

export default {
  name: "NewQuizPage",
  data() {
    return {
      username: ''
    };
  },
  methods: {
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
