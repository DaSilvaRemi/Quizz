<template>
    <table class="table">
        <thead>
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
                    <button class="btn mb-4" type="button" @click="handleClickReadQuestion(question.id)">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn mb-4" type="button" @click="handleClickUpdateQuestion(question.id)">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn mb-4" type="button" data-bs-toggle="modal" data-bs-target="#validation-modal">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
            <ValidationModal titre="Avertissement !" body="Voulez vous supprimer cette question ?"
                @modal-click-btn-ok="handleClickDeleteQuestion(question.id)" />
        </tbody>
    </table>
</template>


<script>
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
            allQuestions: [],
        };
    },
    async created() {
        this.loadAllQuestions()
    },
    methods: {
        handleClickReadQuestion(index) {
            this.$router.push(`/read-question/${index}`);
        },
        handleClickUpdateQuestion(index) {
            this.$router.push(`/edit-question/${index}`);
        },
        async handleClickDeleteQuestion(index) {
            quizApiService.deleteQuestionById(index, this.token)
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