<template>
    <div>
        <h2>Vos questions :</h2>
    </div>

    <ListQuestionsDisplay />

    <div class="text-center">
        <RouterLink to="/create-question" class="btn btn-primary">Créer question</RouterLink>
    </div>
</template>


<script>
import ListQuestionsDisplay from "@/components/ListQuestionsDisplay.vue"

export default {
    name: "ListQuestionsPage",
    components: {
        ListQuestionsDisplay,
    },
};
</script>