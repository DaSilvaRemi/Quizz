<template>
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
</template>

<script>
export default {
    name: "ScoreListDisplay",
    props: {
      registeredScores: Array
    },
  };
</script>