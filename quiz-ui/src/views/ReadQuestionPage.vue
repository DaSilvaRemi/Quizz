<template>
    <AdminTabNav />
    <QuestionCRUForm :question="question" :maxValPosition="maxValPosition" titreForm="Visualiser une question"
        submitButtonText="Retour" :displayResetButton="false" :readOnly="true"
        @submit-question="handleSubmitQuestionEvent" />
</template>
  
<script>
import quizApiService from "@/services/QuizApiService";
import AdminTabNav from "@/components/AdminTabNav.vue";
import QuestionCRUForm from "@/components/QuestionCRUForm.vue";
import participationStorageService from "@/services/ParticipationStorageService.js";


export default {
    name: "ReadQuestionPage",
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
            maxValPosition: 1,
            token: "",
        };
    },
    async created() {
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

                this.maxValPosition = response.data.size;
            }
            ).catch((error) => {
                console.log(error);
            }
            );

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
        handleSubmitQuestionEvent() {
            this.$router.push("/list-questions");
        },
    }
};
</script>