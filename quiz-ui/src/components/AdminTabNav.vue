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
/**
 * Component: AdminTabNav
 * Description: Represents the navigation component for the admin tab.
 *
 * Data:
 *   - routeName: The name of the current route.
 *
 * Methods:
 *   - handleClickLogout: Handles the click event on the logout button and logs out the user by clearing the token and redirecting to the login page.
 */
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
        /**
        * Handles the click event on the logout button and logs out the user by clearing the token and redirecting to the login page.
        */
        handleClickLogout() {
            participationStorageService.saveToken("");
            this.$router.push("/login");
        }
    }
};
</script>