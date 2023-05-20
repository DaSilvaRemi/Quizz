<template>
    <ScoreListDisplay :registeredScores="registeredScores" />
</template>

<script>
/**
 * Component: ScoreListManager
 * Description: Manages and displays a list of registered scores.
 *
 * Imports:
 *   - ScoreListDisplay: The component responsible for displaying the list of scores.
 *   - quizApiService: The service for interacting with the quiz API.
 *
 * Props: None
 *
 * Data:
 *   - registeredScores: [Array] An array of registered scores.
 *
 * Lifecycle Hook:
 *   - created: Called when the component is created. Fetches the registered scores from the quiz API.
 *
 * Methods:
 *   - fetchRegisteredScores: Fetches the registered scores from the quiz API and updates the registeredScores data.
 */
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
        this.getRegisteredScores();
    },
    methods: {
        /**
        * Fetches the registered scores from the quiz API and updates the registeredScores data.
        */
        async getRegisteredScores() {
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
    }
};
</script>