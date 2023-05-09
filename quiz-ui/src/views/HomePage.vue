<template>
  <h1 class="text-center">Home page</h1>
  <table class="table">
    <thead>
      <tr>
        <th scope="col">Nom du joueur</th>
        <th scope="col">Score</th>
      </tr>
    </thead>
    <tbody v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
      <tr>
        <td>{{ scoreEntry.playerName }}</td>
        <td>{{ scoreEntry.score }}</td>
      </tr>
    </tbody>
  </table>
  <div class="text-center">
    <RouterLink to="/new-quiz" class="btn btn-primary">Démarrer le quiz !</RouterLink>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

let registeredScores = []

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: registeredScores
    };
  },
  async created() {
    quizApiService.getQuizInfo()
      .then((response) => {
        if (response.status !== 200) {
          const ERROR = `CODE : ${response.status} getQuestionByPosition`
          console.error(ERROR);
          return Promise.reject(ERROR);
        }

        this.registeredScores = [...response.data.scores];
      }
      ).catch((error) => {
        console.log(error);
      }
      );
  }
};
</script>