<template>
  <div class="nom-joueur-form">
    <form @submit.prevent="submit">
      <h2 class="text-center">Commencer un nouveau quiz</h2>
      <div class="form-group">
        <label for="nom-joueur" class="form-label">Saisissez votre nom : </label>
        <input type="text" class="form-control" id="nom-joueur" name="nom-joueur" placeholder="Votre nom"
          aria-describedby="Le nom qui sera affiché sur la table des scores" v-model="username" required>
      </div>
      <div class="form-group">
        <button type="submit" class="btn btn-primary btn-block" @click="launchNewQuiz">Commencer !</button>
      </div>
    </form>
  </div>
</template>

<script>
import participationStorageService  from "@/services/ParticipationStorageService";

export default {
  name: "NewQuizPage",
  data() {
    return {
      username: participationStorageService.getPlayerName();
    };
  },
  methods: {
    launchNewQuiz(){
      participationStorageService.savePlayerName(this.username);
      this.$router.push('/questions');
    }
  }
};
</script>

<style>
.nom-joueur-form {
  width: 60%;
  margin: 70px auto;
  font-size: 15px;
}

.nom-joueur-form form {
  margin-bottom: 15px;
  background: #f7f7f7;
  box-shadow: 0px 2px 2px 2px rgba(0, 0, 0, 0.4);
  padding: 30px;
}

.nom-joueur-form h2 {
  margin: 0 0 15px;
}

.form-control,
.btn {
  min-height: 38px;
  border-radius: 2px;
}

.btn {
  margin-top: 2%;
  font-size: 15px;
  font-weight: bold;
}
</style>
