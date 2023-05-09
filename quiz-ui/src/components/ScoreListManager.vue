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
    props: {
        getScorePromise: {
            type: Promise,
            default: quizApiService.getQuizInfo()
        }
    },
    data() {
        return {
            registeredScores: []
        };
    },
    async created() {
        this.getScorePromise
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