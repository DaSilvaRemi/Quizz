<template>
  <div class="d-flex align-items-center mx-5 mt-4 mb-2">
    <table class="table table-bordered">
      <thead style="background-color: lightskyblue;">
        <tr>
          <th scope="col">Classement</th>
          <th scope="col">Nom du joueur</th>
          <th scope="col">Score</th>
        </tr>
      </thead>
      <tbody v-for="(scoreEntry, index) in registeredScores" v-bind:key="index">
        <tr :class="{ 'bg-light': index % 2 }">
          <th scope="row">#{{ index + 1 }}</th>
          <td>{{ scoreEntry.playerName }}</td>
          <td>{{ scoreEntry.score }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
/**
 * Component: ScoreListDisplay
 * Description: Displays a list of registered scores.
 *
 * Props:
 *   - registeredScores: [Array] An array of registered scores to be displayed.
 */
export default {
  name: "ScoreListDisplay",
  props: {
    registeredScores: Array
  },
};
</script>