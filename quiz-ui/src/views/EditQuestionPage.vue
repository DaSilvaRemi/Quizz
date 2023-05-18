<template>
    <AdminTabNav />
    <QuestionCRUForm :question="question" titreForm="Editer une question" submitButtonText="Editer" @reset-question="handleResetQuestionEvent" @submit-question="handleSubmitQuestionEvent" />
</template>
  
<script>
import quizApiService from "@/services/QuizApiService";
import AdminTabNav from "@/components/AdminTabNav.vue";
import QuestionCRUForm from "@/components/QuestionCRUForm.vue";
import participationStorageService from "@/services/ParticipationStorageService.js";


export default {
    name: "EditQuestionPage",
    components: {
        AdminTabNav,
        QuestionCRUForm
    },
    data() {
        return {
            question: {
                id: 0,
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
    async created() {
        this.token = participationStorageService.getToken();

        if (!this.token) {
            this.$router.push("/");
            return;
        }
        
        this.question.id = this.$route.params.id;

        quizApiService.getQuestionById(this.question.id).then((response) => {
            if (response.status !== 200) {
                const ERROR = `CODE : ${response.status} postQuestion`
                return Promise.reject(ERROR);
            }

            this.question.titre = response.data.title;
            this.question.intitule = response.data.text;
            this.question.position = response.data.position;
            this.question.image = response.data.image;
            this.question.possibleAnswers = response.data.possibleAnswers;
        }).catch((error) => {
            console.error(error);
            if (error.status === 401) {
                participationStorageService.saveToken("");
                this.$router.push("/login");
            }
        })
    },
    methods: {
        async handleSubmitQuestionEvent(question) {
            console.log(question.possibleAnswers);

            quizApiService.putQuestion(
                this.question.id,
                question.titre,
                question.intitule,
                question.image,
                question.position,
                question.possibleAnswers,
                this.token
            ).then((response) => {
                if (response.status !== 204) {
                    const ERROR = `CODE : ${response.status} putQuestion`
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
        },
        handleResetQuestionEvent() {
            this.$router.push("/list-questions");
        }
    }
};
</script>