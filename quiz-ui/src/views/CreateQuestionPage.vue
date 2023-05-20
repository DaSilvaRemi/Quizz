<template>
    <AdminTabNav />
    <QuestionCRUForm :question="question" :maxValPosition="maxValPosition" titreForm="Créer une question"
        submitButtonText="Créer" :displayResetButton="false" @submit-question="handleSubmitQuestionEvent" />
</template>

<script>
/**
 * Component: CreateQuestionPage
 * Description: Represents the page for creating a new question by the admin.
 *
 * Components:
 *   - AdminTabNav: The navigation component for the admin.
 *   - QuestionCRUForm: The form component for creating or updating a question.
 *
 * Data:
 *   - question: An object representing the new question being created.
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
 *
 * Methods:
 *   - handleSubmitQuestionEvent: Handles the submission of the question form and sends the data to the server.
 */
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

                this.maxValPosition = response.data.size + 1;
            }
            ).catch((error) => {
                console.log(error);
            }
            );
    },
    methods: {
        /**
         * Handles the submission of the question form and sends the data to the server.
         * @param {Object} question - The question data to be submitted.
         */
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