<template>
    <div class="text-center">
        <h2>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h2>
        <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
    </div>
</template>

<script>
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
    methods: {
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

                    participationStorageService.saveParticipationScore(response.data.score);
                    this.$router.push('/score');
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
                    const ERROR = `CODE : ${response.status} getQuizInfo`
                    return Promise.reject(ERROR);
                }

                this.totalNumberOfQuestion = response.data.size;
            }
            ).catch((error) => {
                console.log(error);
            }
            );
        this.loadQuestionByPosition();
    },
}

</script>