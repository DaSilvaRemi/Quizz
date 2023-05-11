<template>
    <ScoreListDisplay :registeredScores="registeredScores" />
</template>

<script>
import ScoreListDisplay from "@/components/ScoreListDisplay.vue";
import quizApiService from "@/services/QuizApiService.js";

export default {
    name: "ScoreListManager",
    components: {
        ScoreListDisplay
    },
    data() {
        return {
            registeredScores: []
        };
    },
    async created() {
        quizApiService.getQuizInfo()
            .then((response) => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} getQuestionByPosition`
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