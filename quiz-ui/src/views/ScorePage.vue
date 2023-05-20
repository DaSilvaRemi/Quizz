<template>
    <div class="text-center" >
        <h2>Votre score : {{ playerScore }}</h2>
    </div>
    <ScoreListManager />
    <div class="text-center mb-4">
        <RouterLink to="/" class="btn btn-primary">Retour à l'accueil</RouterLink>
    </div>
</template>


<script>
/**
 * name: "ScorePage"
 * 
 * Description: A page component for displaying the user's score.
 * 
 * Components:
 * - ScoreListManager: Component for managing and displaying the list of scores.
 * 
 * Data:
 * - playerScore: The score of the player.
 * 
 * Lifecycle hooks:
 * - created(): Lifecycle hook called when the component is created.
 *   Checks if the participation score is available in the participation storage service.
 *   If not available, redirects the user to the home page.
 *   If available, retrieves the score from the participation storage service and assigns it to 'playerScore'.
 *   Clears the participation storage service to reset the score.
 * 
 */
import ScoreListManager from "@/components/ScoreListManager.vue";
import participationStorageService from "@/services/ParticipationStorageService.js";

export default {
    name: "ScorePage",
    components: {
        ScoreListManager
    },
    data() {
        return {
            playerScore: 0
        };
    },
    created() {
        if(!participationStorageService.getParticipationScore()){
            this.$router.push('/home');
        }

        this.playerScore = participationStorageService.getParticipationScore();
        participationStorageService.clear();
    }
};
</script>