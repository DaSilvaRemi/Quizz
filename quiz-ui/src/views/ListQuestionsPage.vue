<template>
    <AdminTabNav />
    <div class="text-center">
        <h2>Vos questions</h2>
    </div>

    <ListQuestionsDisplay :token="token" />

    <div class="text-center">
        <RouterLink to="/create-question" class="btn btn-primary">Créer question</RouterLink>
    </div>
</template>


<script>
import ListQuestionsDisplay from "@/components/ListQuestionsDisplay.vue"
import AdminTabNav from "@/components/AdminTabNav.vue";
import participationStorageService from "@/services/ParticipationStorageService.js";

export default {
    name: "listQuestions",
    components: {
        ListQuestionsDisplay,
        AdminTabNav
    },
    data(){
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