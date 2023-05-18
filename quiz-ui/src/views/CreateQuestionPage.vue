<template>
    <AdminTabNav />
    <QuestionCRUForm 
        :question="question"
        titreForm="Créer une question"
        submitButtonText="Créer"
        @submit-question="handleSubmitQuestionEvent"
    />
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
            token: "",
            error: ""
        };
    },
    created() {
        this.token = participationStorageService.getToken();

        if (!this.token) {
            this.$router.push("/");
            return;
        }
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