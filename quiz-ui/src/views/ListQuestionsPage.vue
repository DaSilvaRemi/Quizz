<template>
    <AdminTabNav />
    <h1 class="text-center my-4">
        Vos questions
    </h1>

    <ListQuestionsDisplay :token="token" />

    <div class="text-center my-3">
        <RouterLink to="/create-question" class="btn btn-primary mb-4">Créer question</RouterLink>
    </div>
</template>


<script>
/**
 * Component: listQuestions
 * Description: Represents the page for listing and managing questions.
 *
 * Components:
 *   - ListQuestionsDisplay: The component for displaying the list of questions.
 *   - AdminTabNav: The navigation component for the admin section.
 *
 * Data:
 *   - token (String): The token for authentication.
 *
 * Methods:
 *   - created(): Lifecycle hook called when the component is created. Retrieves the authentication token and redirects to the home page if the token is missing.
 */
import { RouterLink } from 'vue-router';
import ListQuestionsDisplay from "@/components/ListQuestionsDisplay.vue"
import AdminTabNav from "@/components/AdminTabNav.vue";
import participationStorageService from "@/services/ParticipationStorageService.js";

export default {
    name: "listQuestions",
    components: {
        ListQuestionsDisplay,
        AdminTabNav
    },
    data() {
        return {
            token: ""
        }
    },
    created() {
        this.token = participationStorageService.getToken();

        if (!this.token) {
            this.$router.push("/");
            return;
        }
    },
};
</script>