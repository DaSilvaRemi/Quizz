<template>
    <AdminTabNav />
    <QuestionCRUForm :question="question" :maxValPosition="maxValPosition"
        :titreForm="'Editer la question id : ' + question.id" submitButtonText="Editer"
        @submit-question="handleSubmitQuestionEvent" @reset-question="handleResetQuestionEvent" />
    <ValidationModal titre="Avertissement !" body="Voulez vous éditer cette question ?"
        @modal-click-btn-ok="handleClickEditQuestionButton" />
</template>
  
<script>
/**
 * Component: EditQuestionPage
 * Description: Represents the page for editing an existing question by the admin.
 *
 * Components:
 *   - AdminTabNav: The navigation component for the admin.
 *   - QuestionCRUForm: The form component for creating or updating a question.
 *   - ValidationModal: The modal component for displaying a validation message.
 *
 * Data:
 *   - question: An object representing the question being edited.
 *     - id: The ID of the question.
 *     - titre: The title of the question.
 *     - intitule: The content of the question.
 *     - position: The position of the question.
 *     - image: The image associated with the question.
 *     - possibleAnswers: An array of possible answers for the question.
 *   - maxValPosition: The maximum value for the question position.
 *   - token: The authentication token of the admin.
 *
 * Created:
 *   - Fetches the quiz information to determine the maximum value for the question position.
 *   - Fetches the existing question data to populate the form for editing.
 *
 * Methods:
 *   - handleSubmitQuestionEvent: Handles the submission of the question form and displays a validation modal.
 *   - handleClickEditQuestionButton: Handles the click event of the edit question button and sends the updated question data to the server.
 *   - handleResetQuestionEvent: Handles the reset event of the question form and redirects to the list of questions page.
 */
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService.js";
import AdminTabNav from "@/components/AdminTabNav.vue";
import QuestionCRUForm from "@/components/QuestionCRUForm.vue";
import ValidationModal from "@/components/ValidationModal.vue";


export default {
    name: "EditQuestionPage",
    components: {
        AdminTabNav,
        QuestionCRUForm,
        ValidationModal,
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
         * Handles the submission of the question form and displays a validation modal.
         * @param {Object} question - The question data to be submitted.
         */
        handleSubmitQuestionEvent(question) {
            this.question = question;
            const VALIDATION_MODAL = new bootstrap.Modal(document.getElementById('validation-modal'));
            VALIDATION_MODAL.show();
        },
        /**
         * Handles the click event of the edit question button and sends the updated question data to the server.
         */
        async handleClickEditQuestionButton() {
            quizApiService.putQuestion(
                this.question.id,
                this.question.titre,
                this.question.intitule,
                this.question.image,
                this.question.position,
                this.question.possibleAnswers,
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
        /**
         * Handles the reset event of the question form and redirects to the list of questions page.
         */
        handleResetQuestionEvent() {
            this.$router.push("/list-questions");
        }
    }
};
</script>