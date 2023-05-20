<template>
    <div class="text-center" >
        <h2>Votre score : {{ playerScore }}</h2>
    </div>
    <ScoreListManager />
    <div class="text-center">
        <RouterLink to="/" class="btn btn-primary">Retour à l'accueil</RouterLink>
    </div>
</template>


<script>
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