<template>
    <div class="d-flex flex-column align-items-center pt-3">
        <div class="d-flex flex-row">
            <div class="card" style="width: 18rem;">
                <div class="card-body">
                    <h5 class="card-title">{{ question.title }}</h5>
                    <p class="card-text">{{ question.text }}</p>
                </div>
                <ul class="list-group list-group-flush" v-for="(possibleAnswer, index) in question.possibleAnswers" v-bind:key="possibleAnswer.id">
                    <button class="btn btn-outline-dark m-1" @click="selectAnswer(index)">
                        {{ possibleAnswer.text }}
                    </button>
                </ul>
            </div>
            <div style="margin-left: 10px;">
                <img v-if="question.image" :src="question.image" class="card-img-top" style=" max-height:200px" alt="<Image introuvable...>">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'QuestionDisplay',
    emits: ["answer-selected"],
    props: {
        question: {
            type: Object
        }
    },
    methods: {
        selectAnswer(possibleAnswerIndex) {
            this.$emit('answer-selected', possibleAnswerIndex + 1);
        }
    },
}

</script>