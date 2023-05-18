<template>
    <div class="d-flex flex-column align-items-center pt-5">
        <form @submit.prevent="submit">
            <h2 class="text-center">{{ titreForm }}</h2>
            <div class="form-outline mb-4">
                <label class="form-label" for="titre">Titre</label>
                <input type="text" id="titre" name="titre" class="form-control" placeholder="Mon titre" v-model="question.titre"
                    required />
            </div>

            <div class="form-outline mb-4">
                <label class="form-label" for="intitule">Intitulé</label>
                <textarea id="intitule" name="intitule" class="form-control" placeholder="Mon intitulé"
                    v-model="question.intitule" required></textarea>
            </div>

            <div class="form-outline mb-4">
                <label class="form-label" for="position">Position</label>
                <input type="number" id="position" name="position" class="form-control" min="1" v-model="question.position" />
            </div>

            <img class="img-fluid" :src="question.image" :alt="question.image">

            <div class="form-outline mb-4">
                <ImageUpload @file-change="handleChangeImage" :image="question.image" />
            </div>

            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">Text</th>
                        <th scope="col">isCorrect</th>
                        <th scope="col">Supprimer</th>
                    </tr>
                </thead>
                <tbody v-for="(possibleAnswer, index) in question.possibleAnswers" v-bind:key="index">
                    <tr>
                        <td>
                            <input type="text" id="possibleAnswerTexte" name="possibleAnswerTexte" class="form-control"
                                placeholder="Un texte" v-model="possibleAnswer.text" required />
                        </td>
                        <td>
                            <input class="form-check-input me-2" type="checkbox" id="possibleAnswerisCorrect"
                                name="possibleAnswerisCorrect" v-model="possibleAnswer.isCorrect"
                                @change="handleChangePossibleAnswerIsCorrect(index)" />
                        </td>
                        <td>
                            <button class="btn mb-4" type="button" @click="handleClickDeletePossibleAnswer(index)"><i
                                    class="bi bi-x-circle-fill"></i></button>
                        </td>
                    </tr>
                </tbody>
                <button class="btn mb-4" type="button" @click="handleClickAddPossibleAnswer"><i
                        class="bi bi-plus-circle-fill"></i></button>
            </table>
            <p v-if="error" class="alert alert-danger">{{ error }}</p>
            <div class="text-center">
                <button class="btn btn-primary btn-block mx-4 mb-4" type="submit" @click="handleClickSubmitQuestion">{{
                    submitButtonText }}</button>
                <button v-if="resetButton" class="btn btn-primary btn-block mx- mb-4" type="reset"
                    @click="handleResetQuestion">Annuler</button>
            </div>
        </form>
    </div>
</template>

<script>
import ImageUpload from "@/components/ImageUpload.vue";

export default {
    name: "QuestionCRUForm",
    components: {
        ImageUpload
    },
    props: {
        question: Object,
        titreForm: String,
        submitButtonText: String,
        resetButton: {
            type: Boolean,
            default: true,
        },
    },
    data() {
        return {
            questionCopy: {...this.question},
            error: ""
        };
    },
    methods: {
        handleChangeImage(fileDataUrl) {
            this.question.image = fileDataUrl;
        },
        handleClickAddPossibleAnswer() {
            this.question.possibleAnswers.push({ text: '', isCorrect: false });
        },
        handleClickDeletePossibleAnswer(index) {
            this.question.possibleAnswers.splice(index, 1);
        },
        handleChangePossibleAnswerIsCorrect(index) {
            for (let i = 0; i < this.question.possibleAnswers.length; i++) {
                const POSSIBLE_ANSWER = this.question.possibleAnswers[i];

                if (i !== index) {
                    POSSIBLE_ANSWER.isCorrect = false;
                }
            }
        },
        handleClickSubmitQuestion() {
            let count = 0;
            this.question.possibleAnswers.forEach((possibleAnswer) => {
                if (possibleAnswer.isCorrect) {
                    count++;
                }
            });

            if (count !== 1) {
                this.error = "Une seule des réponses possible doit être bonne !";
                return;
            }

            this.$emit("submit-question", this.question);
        },
        handleResetQuestion() {
            this.$emit("reset-question", this.question);
        },
    }
}
</script>