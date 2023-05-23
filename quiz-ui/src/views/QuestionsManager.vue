<template>
    <div class="text-center">
        <h2>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h2>
        <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
    </div>
</template>

<script>
/**
 * Component: QuestionManager
 * Description: Represents the manager for handling quiz questions.
 *
 * Components:
 *   - QuestionDisplay: Component for displaying a single question.
 *
 * Data:
 *   - currentQuestion (Object): The currently displayed question.
 *   - currentQuestionPosition (Number): The position of the current question.
 *   - totalNumberOfQuestion (Number): The total number of questions in the quiz.
 *   - playerAnswers (Array): The player's answers to the questions.
 *
 * Methods:
 *   - created(): Lifecycle hook called when the component is created. Retrieves the total number of questions in the quiz.
 *   - loadQuestionByPosition(): Loads the question based on the current question position.
 *   - answerClickedHandler(possibleAnswerIndex): Handles the event when a possible answer is clicked.
 *   - endQuiz(): Handles the end of the quiz by saving the player's participation and redirecting to the score page.
 */
import QuestionDisplay from "@/components/QuestionDisplay.vue";
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/services/ParticipationStorageService.js";

export default {
    name: 'QuestionManager',
    components: {
        QuestionDisplay
    },
    data() {
        return {
            currentQuestion: {},
            currentQuestionPosition: 1,
            totalNumberOfQuestion: 1,
            playerAnswers: []
        };
    },
    async created() {
        quizApiService.getQuizInfo()
            .then((response) => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} getQuizInfo`
                    return Promise.reject(ERROR);
                }

                this.totalNumberOfQuestion = response.data.size;

                if(this.totalNumberOfQuestion === 0){
                    this.$router.push('/new-quiz');
                }
            }
            ).catch((error) => {
                console.log(error);
            }
            );
        this.loadQuestionByPosition();
    },
    methods: {
        /**
         * Retrieves the question data from the API response and assigns it to the 'currentQuestion' data property.
         * It is called when the component is created and when the user selects an answer.
         */
        async loadQuestionByPosition() {
            quizApiService.getQuestionByPosition(this.currentQuestionPosition)
                .then((response) => {
                    if (response.status !== 200) {
                        const ERROR = `CODE : ${response.status} getQuestionByPosition`
                        return Promise.reject(ERROR);
                    }
                    
                    this.currentQuestion = response.data;
                }
                ).catch((error) => {
                    console.log(error);
                }
                )
                ;
        },
        /**
         * Adds the index of the clicked answer to the 'playerAnswers' array.
         * If it is the last question, calls the 'endQuiz' method, otherwise, increments the 'currentQuestionPosition' and loads the next question.
         * @param {Number} possibleAnswerIndex - The index of the clicked possible answer.
         */
        async answerClickedHandler(possibleAnswerIndex) {
            this.playerAnswers.push(possibleAnswerIndex);

            if(this.currentQuestionPosition === this.totalNumberOfQuestion){
                return this.endQuiz();
            }
            
            this.currentQuestionPosition++;
            this.loadQuestionByPosition();
        },
        /**
         * Saves the player's participation by sending the player name and answers to the API.
         * If the API response is successful, saves the participation score to the local storage and redirects to the score page.
         * It is called when the user finishes answering all the questions.
         */
        async endQuiz() {
            const PLAYER_NAME = participationStorageService.getPlayerName();
            quizApiService.postParticipation(PLAYER_NAME, this.playerAnswers)
                .then((response) => {
                    if (response.status !== 200) {
                        const ERROR = `CODE : ${response.status} postParticipation`
                        return Promise.reject(ERROR);
                    }

                    participationStorageService.saveParticipationScore(response.data.score);
                    this.$router.push('/score');
                }
                ).catch((error) => {
                    console.log(error);
                }
                );
        }
    }
}
</script>