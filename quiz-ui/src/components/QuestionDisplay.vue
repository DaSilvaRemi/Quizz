<template>
    <div class="card" style="width: 18rem;">
        <div class="card-header">
            <h6>Question n°{{ question.position }}</h6>
        </div>
        <img v-if="question.image" :src="question.image" class="card-img-top" alt="question.image">
        <div class="card-body">
            <h5 class="card-title">{{ question.titre }}</h5>
            <p class="card-text">{{ question.text }}</p>
            <ul class="list-group list-group-flush" v-for="(index, possibleAnswer) in question.possibleAnswers"
                v-bind:key="possibleAnswer.id">
                <li class="list-group-item" @click="selectAnswer(index)">{{ possibleAnswer.text }}
                </li>
            </ul>
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