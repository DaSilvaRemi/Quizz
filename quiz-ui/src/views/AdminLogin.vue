<template>
    <div class="d-flex flex-column align-items-center pt-5">
        <form class="w-25" @submit.prevent="submit">
            <h2 class="text-center mb-4">Se connecter</h2>
            <div class="form-outline mb-4">
              <input class="form-control" type="password" id="mot-de-passe"  placeholder="Mot de passe..." required v-model="password" />
            </div>

            <div class="text-center">
                <button type="submit" class="btn btn-primary btn-block mb-5 w-100" @click="login">Connexion</button>
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

                    if (response.status !== 200) {
                        const ERROR = `CODE : ${response.status} postQuestion`
                        return Promise.reject(ERROR);
                    }

                    participationStorageService.saveToken(response.data.token);
                    this.$router.push('/list-questions');
                })
                .catch((error) => {
                    console.error(error);
                });
        }
    }
};
</script>