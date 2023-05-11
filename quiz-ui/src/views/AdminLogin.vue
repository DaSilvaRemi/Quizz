<template>
    <h1>Se connecter</h1>
    <form @submit.prevent="submit">
        <!-- Password input -->
        <div class="form-outline mb-4">
            <input type="password" id="form2Example2" class="form-control" required v-model="password" />
            <label class="form-label" for="form2Example2">Password</label>
        </div>

        <!-- Submit button -->
        <button type="submit" class="btn btn-primary btn-block mb-4" @click="login">Connexion</button>
    </form>

    <!-- Alerte mauvais mot de passe -->
    <p v-if="error" class="alert alert-danger">Mot de passe incorrect</p>
</template>

<script>
import quizApiService from "@/services/QuizApiService.js";

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
                    };
                    console.log(response)
                    this.$router.push('/list-question-page');
                })
                .catch(e => console.error(e));
        }
    }
};
</script>