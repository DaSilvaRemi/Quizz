<template>
    <AdminTabNav />
    <QuestionCRUForm :question="question" :maxValPosition="maxValPosition" :titreForm="'Visualiser la question id : ' + question.id"
        submitButtonText="Editer" resetButtonText="Supprimer" :readOnly="true" :resetButtonShowModal="true"
        @submit-question="handleSubmitQuestionEvent" />
    <ValidationModal titre="Avertissement !" body="Voulez vous supprimer cette question ?"
        @modal-click-btn-ok="handleClickDeleteQuestionButton(question.id)" />
</template>
  
<script>
/**
 * name: "ReadQuestionPage"
 * 
 * Description: A component for reading and displaying a single question.
 * 
 * Components:
 * - AdminTabNav: Component for displaying the navigation bar for admin users.
 * - QuestionCRUForm: Component for displaying and managing the question form.
 * - ValidationModal: Component for displaying a validation modal.
 * 
 * Data:
 * - question: Object representing the question data, including its id, title, text, position, image, and possible answers.
 * - maxValPosition: The maximum value for the question position.
 * - token: The token retrieved from the participation storage service.
 * 
 * Lifecycle hooks:
 * - created(): Lifecycle hook called when the component is created. Retrieves the quiz information and the question data from the API. 
 *   Sets the 'maxValPosition' based on the quiz size. Redirects to the login page if the user is not authenticated.
 *   If successful, sets the question data (id, title, text, position, image, possible answers) retrieved from the API.
 * 
 * Methods:
 * - handleSubmitQuestionEvent(): Redirects the user to the edit question page for the current question.
 * 
 * - handleClickDeleteQuestionButton(id): Handles the event when the delete question button is clicked.
 *   Deletes the question by its ID using the API service and the authentication token.
 *   If the deletion is successful, redirects the user to the list of questions page.
 *   If the user is not authenticated, redirects to the login page.
 * 
 */
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
        /**
         * handleSubmitQuestionEvent(): Handles the event when the "Edit" button is clicked.
         * Redirects to the edit question page with the current question ID.
         */
        handleSubmitQuestionEvent() {
            this.$router.push(`/edit-question/${this.question.id}`);
        },
        /**
         * handleClickDeleteQuestionButton(id): Handles the event when the "Delete" button is clicked.
         * Deletes the question with the specified ID from the API.
         * If the API response is successful (204 status), redirects to the list questions page.
         * @param {Number} id - The ID of the question to be deleted.
         * @throws {ERROR} - If the API response is not successful or the user is not authorized (401 status).
         */
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