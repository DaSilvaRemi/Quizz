<template>
    <AdminTabNav />
    <QuestionCRUForm :question="question" :maxValPosition="maxValPosition" :titreForm="'Visualiser la question id : ' + question.id"
        submitButtonText="Editer" resetButtonText="Supprimer" :readOnly="true" :resetButtonShowModal="true"
        @submit-question="handleSubmitQuestionEvent" />
    <ValidationModal titre="Avertissement !" body="Voulez vous éditer cette question ?"
        @modal-click-btn-ok="handleClickDeleteQuestionButton(question.id)" />
</template>
  
<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService.js";
import AdminTabNav from "@/components/AdminTabNav.vue";
import QuestionCRUForm from "@/components/QuestionCRUForm.vue";
import ValidationModal from "@/components/ValidationModal.vue";


export default {
    name: "ReadQuestionPage",
    components: {
        AdminTabNav,
        QuestionCRUForm,
        ValidationModal
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
            this.$router.push(`/edit-question/${this.question.id}`);
        },
        handleClickDeleteQuestionButton(id){
            quizApiService.deleteQuestionById(id, this.token)
                .then(response => {
                    if (response.status !== 204) {
                        const ERROR = `CODE : ${response.status} postQuestion`
                        return Promise.reject(ERROR);
                    }

                    this.$router.push("/list-questions");
                }
                ).catch((error) => {
                    console.error(error);
                    if (error.status === 401) {
                        participationStorageService.saveToken("");
                        this.$router.push("/login");
                    }
                });
        }
    }
};
</script>