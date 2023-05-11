<template>
    <table class="table">
    <thead>
          <tr>
            <th scope="col">Classement</th>
            <th scope="col">Nom du joueur</th>
            <th scope="col">Score</th>
          </tr>
        </thead>
        <tbody v-for="(scoreEntry, index) in registeredScores" v-bind:key="index">
          <tr>
            <th scope="row">{{ index + 1 }}</th>
            <td>{{ scoreEntry.playerName }}</td>
            <td>{{ scoreEntry.score }}</td>
          </tr>
        </tbody>
    </table>
</template>

<script>
export default {
    name: "ScoreListDisplay",
    props: {
      registeredScores: Array
    },
  };
</script>