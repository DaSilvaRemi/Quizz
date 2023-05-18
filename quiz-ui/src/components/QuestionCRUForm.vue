<template>
    <div class="d-flex flex-column align-items-center pt-5">
        <form @submit.prevent="submit">
            <h2 class="text-center">{{ titreForm }}</h2>
            <div class="form-outline mb-4">
                <label class="form-label" for="titre">Titre</label>
                <input type="text" id="titre" name="titre" class="form-control" placeholder="Mon titre" v-model="form.titre"
                    required />
            </div>

            <div class="form-outline mb-4">
                <label class="form-label" for="intitule">Intitulé</label>
                <textarea id="intitule" name="intitule" class="form-control" placeholder="Mon intitulé"
                    v-model="form.intitule" required></textarea>
            </div>

            <div class="form-outline mb-4">
                <label class="form-label" for="position">Position</label>
                <input type="number" id="position" name="position" class="form-control" min="1" v-model="form.position" />
            </div>

            <img class="img-fluid" :src="form.image" :alt="form.image">

            <div class="form-outline mb-4">
                <ImageUpload @file-change="handleChangeImage" :image="form.image" />
            </div>

            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">Text</th>
                        <th scope="col">isCorrect</th>
                        <th scope="col">Supprimer</th>
                    </tr>
                </thead>
                <tbody v-for="(possibleAnswer, index) in form.possibleAnswers" v-bind:key="index">
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
            <div class="btn-group" role="group" aria-label="Basic example">
                <div class="text-center">
                    <button class="btn btn-primary btn-block mb-4" type="submit" @click="handleClickSubmitQuestion">{{
                        submitButtonText }}</button>
                </div>
                <div class="text-center">
                    <button class="btn btn-primary btn-block mb-4" type="reset" @click="handleResetQuestion">Annuler</button>
                </div>
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
        titre: String,
        intitule: String,
        position: Number,
        image: String,
        possibleAnswers: Array,
        titreForm: String,
        submitButtonText: String,
    },
    data() {
        return {
            form: {
                titre: this.titre,
                intitule: this.intitule,
                position: this.position,
                image: this.image,
                possibleAnswers: [...this.possibleAnswers]
            },
            error: ""
        };
    },

    updated(){
        this.form =  {
                titre: this.titre,
                intitule: this.intitule,
                position: this.position,
                image: this.image,
                possibleAnswers: [...this.possibleAnswers]
            }
    },
    
    methods: {
        handleChangeImage(fileDataUrl) {
            this.form.image = fileDataUrl;
        },
        handleClickAddPossibleAnswer() {
            this.form.possibleAnswers.push({ text: '', isCorrect: false });
        },
        handleClickDeletePossibleAnswer(index) {
            this.form.possibleAnswers.splice(index, 1);
        },
        handleChangePossibleAnswerIsCorrect(index) {
            for (let i = 0; i < this.form.possibleAnswers.length; i++) {
                const POSSIBLE_ANSWER = this.form.possibleAnswers[i];

                if (i !== index) {
                    POSSIBLE_ANSWER.isCorrect = false;
                }
            }
        },
        handleClickSubmitQuestion() {
            let count = 0;
            this.form.possibleAnswers.forEach((possibleAnswer) => {
                if (possibleAnswer.isCorrect) {
                    count++;
                }
            });

            if (count !== 1) {
                this.error = "Une seule des réponses possible doit être bonne !";
                return;
            }

            this.$emit("submit-question", this.form);
        },
        handleResetQuestion(){
            this.$emit("reset-question", this.form);
           
        }
    }
}
</script>