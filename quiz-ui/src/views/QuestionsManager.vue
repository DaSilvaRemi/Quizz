<template>
    <div class="text-center">
        <p>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</p>
        <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
    </div>
</template>

<script>
import QuestionDisplay from "@/components/QuestionDisplay.vue"
import quizApiService from "@/services/QuizApiService.js"
import participationStorageService from "@/services/ParticipationStorageService";

export default {
    name: 'QuestionManager',
    components: {
        QuestionDisplay
    },
    data() {
        return {
            currentQuestion: null,
            currentQuestionPosition: 1,
            totalNumberOfQuestion: 1,
            playerAnswers: []
        };
    },
    methods: {
        async loadQuestionByPosition() {
            quizApiService.getQuestionByPosition(this.currentQuestionPosition)
                .then((response) => {
                    if (response.status !== 200) {
                        const ERROR = `CODE : ${response.status} getQuestionByPosition`
                        return Promise.reject(ERROR);
                    }

                    this.currentQuestion = response;
                }
                ).catch((error) => {
                    console.log(error)
                }
                )
                ;
        },
        async answerClickedHandler(possibleAnswerIndex) {
            this.playerAnswers.push(possibleAnswerIndex);

            if(this.currentQuestionPosition === this.totalNumberOfQuestion){
                return this.endQuiz();
            }
            
            this.currentQuestionPosition++;
            this.loadQuestionByPosition();
        },
        async endQuiz() {
            const PLAYER_NAME = participationStorageService.getPlayerName();
            quizApiService.postParticipation(PLAYER_NAME, this.playerAnswers)
                .then((response) => {
                    if (response.status !== 200) {
                        const ERROR = `CODE : ${response.status} postParticipation`
                        return Promise.reject(ERROR);
                    }

                    this.$router.push('/home');
                }
                ).catch((error) => {
                    console.log(error);
                }
                );
        }
    },
    async created() {
        quizApiService.getQuizInfo()
            .then((response) => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} getQuestionByPosition`
                    console.error(ERROR);
                    return Promise.reject(ERROR);
                }

                this.totalNumberOfQuestion = response.size;
            }
            ).catch((error) => {
                console.log(error);
            }
            );
    },
}

</script>