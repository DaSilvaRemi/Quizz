<template>
    <div class="d-flex flex-column align-items-center pt-5">
        <form class="w-25" @submit.prevent="login">
            <h2 class="text-center mb-4">Se connecter</h2>
            <div class="form-outline mb-4">
              <input class="form-control" type="password" id="mot-de-passe"  placeholder="Mot de passe..." required v-model="password" />
            </div>

            <div class="text-center">
                <button type="submit" class="btn btn-primary btn-block mb-5 w-100">Connexion</button>
            </div>
        </form>

        <!-- Alerte mauvais mot de passe -->
        <p v-if="error" class="alert alert-danger">Mot de passe incorrect</p>
    </div>
</template>

<script>
/**
 * Component: AdminLogin
 * Description: Represents the login component for the admin.
 *
 * Data:
 *   - password: The password entered by the admin.
 *   - error: Indicates if there was an error during the login process.
 *
 * Methods:
 *   - login: Performs the login process by sending the password to the server and handling the response.
 */
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
        /**
         * Performs the login process by sending the password to the server and handling the response.
         */
        login() {
            if(!this.password){
                return;
            }

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