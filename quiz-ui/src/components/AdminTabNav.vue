<template>
    <ul class="nav nav-tabs">
        <li class="nav-item">
            <RouterLink v-if="routeName === 'listQuestions'" class="nav-link active" to="/list-questions">
                Toutes les questions
            </RouterLink>
            <RouterLink v-else class="nav-link" to="/list-questions">
                Toutes les questions
            </RouterLink>
        </li>
        <li class="nav-item">
            <RouterLink v-if="routeName === 'createQuestion'" class="nav-link active" to="/create-question">
                Nouvelle question
            </RouterLink>
            <RouterLink v-else class="nav-link" to="/create-question">
                Nouvelle question
            </RouterLink>
        </li>
        <li class="nav-item">
            <button class="nav-link" @click="handleClickLogout">Déconnexion</button>
        </li>
    </ul>
</template>

<script>
import { RouterLink } from 'vue-router';
import participationStorageService from "@/services/ParticipationStorageService.js";

export default {
    name: "AdminTabNav",
    data(){
        return{
            routeName: this.$route.name
        }
    },
    methods: {
        handleClickLogout() {
            participationStorageService.saveToken("");
            this.$router.push("/login");
        }
    }
};
</script>