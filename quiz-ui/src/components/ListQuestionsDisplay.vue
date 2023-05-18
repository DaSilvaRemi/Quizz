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
                    <button class="btn mb-4" type="button" @click="handleClickUpdateQuestion(question.id)">
                        <i class="bi bi-eye"></i>
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn mb-4" type="button" @click="handleClickDeleteQuestion(question.id)">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        </tbody>
    </table>
</template>


<script>
import quizApiService from "@/services/QuizApiService.js";
export default {
    name: "ListQuestionsDisplay",
    data() {
        return {
            allQuestions: [],
        };
    },
    created() {
        quizApiService
            .getAllQuestions()
            .then(response => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} getAllQuestions`
                    return Promise.reject(ERROR);
                }
                this.allQuestions = [...response.data.questions];
                console.log(this.allQuestions);
            });
    },
    methods: {
        handleClickUpdateQuestion(index) {
            this.$router.push(`/questions/${index}`);
        },
        handleClickDeleteQuestion(index) {
            quizApiService.deleteQuestionById(index);
        },
    },
}
</script>