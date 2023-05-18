<template>
    <AdminTabNav />
    <QuestionCRUForm :question="question" :maxValPosition="maxValPosition" titreForm="Créer une question"
        submitButtonText="Créer" :displayResetButton="false" @submit-question="handleSubmitQuestionEvent" />
</template>

<script>
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/services/ParticipationStorageService.js";
import AdminTabNav from "@/components/AdminTabNav.vue";
import QuestionCRUForm from "@/components/QuestionCRUForm.vue";

export default {
    name: "CreateQuestionPage",
    components: {
        AdminTabNav,
        QuestionCRUForm
    },
    data() {
        return {
            question: {
                titre: "",
                intitule: "",
                position: 1,
                image: "",
                possibleAnswers: [],
            },
            maxValPosition: 1,
            token: "",
        };
    },
    created() {
        this.token = participationStorageService.getToken();

        if (!this.token) {
            this.$router.push("/");
            return;
        }

        quizApiService.getQuizInfo()
            .then((response) => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} getQuizInfo`
                    return Promise.reject(ERROR);
                }

                this.maxValPosition = response.data.size + 1;
            }
            ).catch((error) => {
                console.log(error);
            }
            );
    },
    methods: {
        async handleSubmitQuestionEvent(question) {
            quizApiService.postQuestion(
                question.titre,
                question.intitule,
                question.image,
                question.position,
                question.possibleAnswers,
                this.token
            ).then((response) => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} postQuestion`
                    return Promise.reject(ERROR);
                }

                this.$router.push("/list-questions");
            }).catch((error) => {
                console.error(error);
                if (error.status === 401) {
                    participationStorageService.saveToken("");
                    this.$router.push("/login");
                }
            })
        }
    }
}

</script>