<template>
    <div class="d-flex flex-column align-items-center pt-5">
        <h1>Se connecter</h1>

        <form style="width: 22rem;" @submit.prevent="submit">
            <!-- Password input -->
            <div class="form-outline mb-4">
                <input type="password" id="form2Example2" class="form-control" placeholder="Mot de passe..." required v-model="password" />
            </div>

            <!-- Submit button -->
            <div class="text-center">
                <button type="submit" class="btn btn-primary btn-block mb-4" @click="login">Connexion</button>
            </div>
        </form>

        <!-- Alerte mauvais mot de passe -->
        <p v-if="error" class="alert alert-danger">Mot de passe incorrect</p>
    </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/services/ParticipationStorageService.js";

export default {
    name: "AdminLogin",
    data() {
        return {
            password: '',
            error: false,
        };
    },
    methods: {
        login() {
            quizApiService
                .postLogin(this.password)
                .then(response => {
                        if (!response) {
                            this.error = true;
                            return;
                        }

                        console.log(response);
                        participationStorageService.saveToken(response.data.token);
                        this.$router.push('/list-question-page');
                    })
                .catch(e => console.error(e));
        }
    }
};
</script>