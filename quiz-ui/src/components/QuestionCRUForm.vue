<template>
    <div class="d-flex flex-column align-items-center pt-5">
        <form @submit.prevent="handleClickSubmitQuestion">
            <h2 class="text-center">{{ titreForm }}</h2>
            <div class="form-outline mb-4">
                <label class="form-label" for="titre">Titre</label>
                <input type="text" id="titre" name="titre" class="form-control" placeholder="Mon titre"
                    v-model="questionCopy.titre" required :disabled="readOnly" />
            </div>

            <div class="form-outline mb-4">
                <label class="form-label" for="intitule">Intitulé</label>
                <textarea id="intitule" name="intitule" class="form-control" placeholder="Mon intitulé"
                    v-model="questionCopy.intitule" required :disabled="readOnly"></textarea>
            </div>

            <div class="form-outline mb-4">
                <label class="form-label" for="position">Position</label>
                <input type="number" id="position" name="position" class="form-control" min="1" :max="maxValPosition"
                    v-model="questionCopy.position" :disabled="readOnly" />
            </div>

            <img class="img-fluid" :src="questionCopy.image" :alt="questionCopy.image" :disabled="readOnly">

            <div class="form-outline mb-4">
                <ImageUpload @file-change="handleChangeImage" :image="questionCopy.image" :readOnly="readOnly" />
            </div>

            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">Text</th>
                        <th scope="col">isCorrect</th>
                        <th scope="col" v-if="!readOnly">Supprimer</th>
                    </tr>
                </thead>
                <tbody v-for="(possibleAnswer, index) in questionCopy.possibleAnswers" v-bind:key="index">
                    <tr>
                        <td>
                            <input type="text" id="possibleAnswerTexte" name="possibleAnswerTexte" class="form-control"
                                placeholder="Un texte" v-model="possibleAnswer.text" required :disabled="readOnly" />
                        </td>
                        <td>
                            <input class="form-check-input me-2" type="checkbox" id="possibleAnswerisCorrect"
                                name="possibleAnswerisCorrect" v-model="possibleAnswer.isCorrect"
                                @change="handleChangePossibleAnswerIsCorrect(index)" :disabled="readOnly" />
                        </td>
                        <td v-if="!readOnly">
                            <button class="btn mb-4" type="button" @click="handleClickDeletePossibleAnswer(index)"><i
                                    class="bi bi-x-circle-fill"></i></button>
                        </td>
                    </tr>
                </tbody>
                <button v-if="!readOnly" class="btn mb-4" type="button" @click="handleClickAddPossibleAnswer"><i
                        class="bi bi-plus-circle-fill"></i></button>
            </table>
            <p v-if="error" class="alert alert-danger">{{ error }}</p>
            <div class="text-center">
                <button class="btn btn-primary btn-block mx-4 mb-4" type="submit" :data-bs-toggle="submitButtonShowModal ? 'modal' : ''" data-bs-target="#validation-modal">{{
                        submitButtonText }}</button>
                <button v-if="displayResetButton" class="btn btn-primary btn-block mx- mb-4" type="reset"
                    :data-bs-toggle="resetButtonShowModal ? 'modal' : ''" data-bs-target="#validation-modal"
                    @click="handleResetQuestion">{{ resetButtonText }}</button>
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
        maxValPosition: Number,
        titreForm: String,
        submitButtonText: String,
        resetButtonText: {
            type: String,
            default: "Annuler"
        },
        displayResetButton: {
            type: Boolean,
            default: true,
        },
        readOnly: {
            type: Boolean,
            default: false,
        },
        submitButtonShowModal: {
            type: Boolean,
            default: false,
        },
        resetButtonShowModal: {
            type: Boolean,
            default: false,
        }
    },
    data() {
        return {
            questionCopy: {...this.question, possibleAnswers: [...this.question.possibleAnswers] },
            error: ""
        };
    },
    watch: { 
        question: {
            handler(newVal, oldVal) {
                this.questionCopy = {...newVal, possibleAnswers: [...newVal.possibleAnswers] };
            },
            deep: true,
            immediate: true,
        },
    },
    methods: {
        handleChangeImage(fileDataUrl) {
            this.questionCopy.image = fileDataUrl;
        },
        handleClickAddPossibleAnswer() {
            this.questionCopy.possibleAnswers.push({ text: '', isCorrect: false });
        },
        handleClickDeletePossibleAnswer(index) {
            this.questionCopy.possibleAnswers.splice(index, 1);
        },
        handleChangePossibleAnswerIsCorrect(index) {
            for (let i = 0; i < this.questionCopy.possibleAnswers.length; i++) {
                const POSSIBLE_ANSWER = this.questionCopy.possibleAnswers[i];

                if (i !== index) {
                    POSSIBLE_ANSWER.isCorrect = false;
                }
            }
        },
        handleClickSubmitQuestion() {
            if (!this.questionCopy.titre || !this.questionCopy.intitule || this.questionCopy.position < 1 || this.questionCopy.position > this.maxValPosition || !this.questionCopy.image) {
                return;
            }

            let count = 0;
            let possibelAnswersIsValid = true;
            this.questionCopy.possibleAnswers.forEach((possibleAnswer) => {
                if (!possibleAnswer.text) {
                    possibelAnswersIsValid = false;
                    return;
                }

                if (possibleAnswer.isCorrect) {
                    count++;
                }
            });

            if (!possibelAnswersIsValid) {
                return;
            }

            if (count !== 1) {
                this.error = "Une seule des réponses possible doit être bonne !";
                return;
            }

            this.$emit("submit-question", this.questionCopy);
        },
        handleResetQuestion() {
            this.$emit("reset-question", this.questionCopy);
        },
    }
}
</script>