<template>
    <QuestionCRUForm :titre="titre" :intitule="intitule" :position="position" :image="image"
        :possibleAnswers="possibleAnswers" titreForm="Créer une question" submitButtonText="Créer"
        @submit-question="handleSubmitQuestionEvent" />
</template>

<script>
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/services/ParticipationStorageService.js";
import QuestionCRUForm from "@/components/QuestionCRUForm.vue";

export default {
    name: "CreateQuestionPage",
    components: {
        QuestionCRUForm
    },
    data() {
        return {
            titre: "",
            intitule: "",
            position: 1,
            image: "",
            possibleAnswers: [],
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
        async handleSubmitQuestionEvent(form) {
            quizApiService.postQuestion(
                form.titre,
                form.intitule,
                form.image,
                form.position,
                form.possibleAnswers,
                this.token
            ).then((response) => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} getQuestionByPosition`
                    return Promise.reject(ERROR);
                }

                this.$router.push("list-questions-page");
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