<template>
    <div class="d-flex flex-column align-items-center pt-5">
        <form @submit.prevent="submit">
            <h2 class="text-center">Créer une question</h2>
            <div class="form-outline mb-4">
                <label class="form-label" for="titre">Titre</label>
                <input type="text" id="titre" name="titre" class="form-control" placeholder="Mon titre" v-model="titre"
                    required />
            </div>

            <div class="form-outline mb-4">
                <label class="form-label" for="intitule">Intitulé</label>
                <textarea id="intitule" name="intitule" class="form-control" placeholder="Mon intitulé" v-model="intitule"
                    required></textarea>
            </div>

            <div class="form-outline mb-4">
                <label class="form-label" for="position">Position</label>
                <input type="number" id="position" name="position" class="form-control" min="1" v-model="position" />
            </div>

            <img class="img-fluid" :src="image" :alt="image">

            <div class="form-outline mb-4">
                <ImageUpload @file-change="handleChangeImage" />
            </div>

            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">Text</th>
                        <th scope="col">isCorrect</th>
                        <th scope="col">Supprimer</th>
                    </tr>
                </thead>
                <tbody v-for="(possibleAnswer, index) in possibleAnswers" v-bind:key="index">
                    <tr>
                        <td>
                            <input type="text" id="possibleAnswerTexte" name="possibleAnswerTexte" class="form-control"
                                placeholder="Un texte" v-model="possibleAnswer.text" required />
                        </td>
                        <td>
                            <input class="form-check-input me-2" type="checkbox" id="possibleAnswerisCorrect"
                                name="possibleAnswerisCorrect" v-model="possibleAnswer.isCorrect" @change="handleChangePossibleAnswerIsCorrect(index)" />
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
                <button class="btn btn-primary btn-block mb-4" type="submit" @click="handleClickCreateQuestion">Créer</button>
            </div>
            
        </form>
    </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/services/ParticipationStorageService.js";
import ImageUpload from "@/components/ImageUpload.vue";

export default {
    name: "CreateQuestionPage",
    components: {
        ImageUpload
    },
    data() {
        return {
            titre: "",
            intitule: "",
            position: 1,
            image: "",
            possibleAnswers: [],
            token: "",
            error: ""
        };
    },
    created() {
        this.token = participationStorageService.getToken();

        if (!this.token) {
            this.$router.push("/");
            return;
        }
    },
    methods: {
        handleChangeImage(fileDataUrl) {
            this.image = fileDataUrl;
        },
        handleClickAddPossibleAnswer() {
            this.possibleAnswers.push({ text: '', isCorrect: false });
        },
        handleClickDeletePossibleAnswer(index) {
            this.possibleAnswers.splice(index, 1);
        },
        handleChangePossibleAnswerIsCorrect(index) {
            for (let i = 0; i < this.possibleAnswers.length; i++) {
                const POSSIBLE_ANSWER = this.possibleAnswers[i];

                if(i !== index){
                    POSSIBLE_ANSWER.isCorrect = false;
                }
            }
        },
        handleClickCreateQuestion() {
            
            let count = 0;
            this.possibleAnswers.forEach((possibleAnswer) => {
                if (possibleAnswer.isCorrect) {
                    count++;
                }
            });

            if(count !== 1){
                this.error = "Une seule des réponses possible doit être bonne !";
                return;
            }

            quizApiService.postQuestion(
                this.titre,
                this.intitule,
                this.image,
                this.position,
                this.possibleAnswers,
                this.token
            ).then((response) => {
                if (response.status !== 200) {
                    const ERROR = `CODE : ${response.status} getQuestionByPosition`
                    return Promise.reject(ERROR);
                }

                this.$router.push("list-question-page");
            }).catch((error) => {
                console.error(error);
                if(error.status === 401){
                    participationStorageService.saveToken("");
                    this.$router.push("/login");
                }
            })

            
        }
    }
}

</script>