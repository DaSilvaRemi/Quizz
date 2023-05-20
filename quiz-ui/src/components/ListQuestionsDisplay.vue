<template>
    <div class="mx-5 mt-4 mb-2">
    <table class="table table-bordered">
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Titre</th>
                <th scope="col">Question</th>
                <th scope="col" style="width: 10%">Image</th>
                <th scope="col">Position</th>
                <th scope="col" style="width: 20%">Actions</th>
            </tr>
        </thead>
        <tbody v-for="(question, index) in allQuestions" v-bind:key="index">
            <tr>
                <td>{{ question.id }}</td>
                <td>{{ question.title }}</td>
                <td>{{ question.text }}</td>
                <td>
                    <img class=" img-fluid" :src=question.image :alt="question.image" />
                </td>
                <td>{{ question.position }}</td>
                <td>
                    <button class="btn m-1" type="button" @click="handleClickReadQuestion(question.id)">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn m-1" type="button" @click="handleClickUpdateQuestion(question.id)">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn mb-1" type="button" data-bs-toggle="modal"
                        :data-bs-target="'#validation-modal-' + question.id">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
            <ValidationModal titre="Avertissement !" :body="'Voulez vous supprimer la question  ' + question.id + ' ?'"
                :id="'validation-modal-' + question.id" @modal-click-btn-ok="handleClickDeleteQuestion(question.id)" />
        </tbody>
    </table>
    </div>
</template>

<script>
/**
 * Component: ListQuestionsDisplay
 * Description: A component for displaying a list of questions.
 *
 * Props:
 *   - token: [String] The authentication token. Default: ""
 *
 * Components:
 *   - ValidationModal: The modal component for validation purposes.
 *
 * Data:
 *   - allQuestions: [Array] An array of all the questions.
 *
 * Methods:
 *   - handleClickReadQuestion(id): Handles the click event to navigate to the read question page.
 *     @param {Number} id - The ID of the question.
 *
 *   - handleClickUpdateQuestion(id): Handles the click event to navigate to the edit question page.
 *     @param {Number} id - The ID of the question.
 *
 *   - handleClickDeleteQuestion(id): Handles the click event to delete a question.
 *     @param {Number} id - The ID of the question.
 *
 *   - loadAllQuestions(): Loads all the questions from the server.
 */
import participationStorageService from "@/services/ParticipationStorageService.js";
import ValidationModal from "@/components/ValidationModal.vue"
import quizApiService from "@/services/QuizApiService.js";
export default {
    name: "ListQuestionsDisplay",
    components: {
        ValidationModal
    },
    props: {
        token: String
    },
    data() {
        return {
            allQuestions: []
        };
    },
    async created() {
        this.loadAllQuestions();
    },
    methods: {
        /**
         * Handles the click event to navigate to the read question page.
         * @param {Number} id - The ID of the question.
         */
        handleClickReadQuestion(id) {
            this.$router.push(`/read-question/${id}`);
        },
        /**
         * Handles the click event to navigate to the edit question page.
         * @param {Number} id - The ID of the question.
         */
        handleClickUpdateQuestion(id) {
            this.$router.push(`/edit-question/${id}`);
        },
        /**
         * Handles the click event to delete a question.
         * @param {Number} id - The ID of the question.
         */
        async handleClickDeleteQuestion(id) {
            quizApiService.deleteQuestionById(id, this.token)
                .then(response => {
                    if (response.status !== 204) {
                        const ERROR = `CODE : ${response.status} postQuestion`
                        return Promise.reject(ERROR);
                    }

                    this.loadAllQuestions();
                }
                ).catch((error) => {
                    console.error(error);
                    if (error.status === 401) {
                        participationStorageService.saveToken("");
                        this.$router.push("/login");
                    }
                });
        },
        /**
         * Loads all the questions from the server.
         */
        async loadAllQuestions() {
            quizApiService
                .getAllQuestions()
                .then(response => {
                    if (response.status !== 200) {
                        const ERROR = `CODE : ${response.status} getAllQuestions`
                        return Promise.reject(ERROR);
                    }
                    this.allQuestions = [...response.data.questions];
                }).catch((error) => {
                    console.error("error", error);
                });
        }
    },
}
</script>