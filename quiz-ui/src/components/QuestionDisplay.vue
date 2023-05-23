<template>
    <div class="d-flex flex-column align-items-center pt-3">
        <div class="d-flex flex-row">
            <div class="card" style="width: 24rem;">
                <div class="card-body">
                    <h5 class="card-title">{{ question.title }}</h5>
                    <p class="card-text">{{ question.text }}</p>
                </div>
                <ul class="list-group list-group-flush" v-for="(possibleAnswer, index) in question.possibleAnswers"
                    v-bind:key="possibleAnswer.id">
                    <button class="btn btn-outline-dark m-1" @click="selectAnswer(index)">
                        {{ possibleAnswer.text }}
                    </button>
                </ul>
            </div>
        </div>
        <div style="margin-left: 10px;">
            <img v-if="question.image" :src="question.image" class="card-img-top" style="max-width:400px"
                alt="<Image introuvable...>">
        </div>
    </div>
</template>

<script>
/**
 * Component: QuestionDisplay
 * Description: Displays a question and handles answer selection.
 *
 * Emits:
 *   - answer-selected: Emitted when an answer is selected.
 *
 * Props:
 *   - question: [Object] The question object to be displayed.
 *
 * Methods:
 *   - selectAnswer(possibleAnswerIndex): Selects an answer and emits the "answer-selected" event.
 *     @param {Number} possibleAnswerIndex - The index of the selected possible answer (1-based index).
 */
export default {
    name: 'QuestionDisplay',
    emits: ["answer-selected"],
    props: {
        question: {
            type: Object
        }
    },
    methods: {
        /**
         * Selects an answer and emits the "answer-selected" event.
         * @param {Number} possibleAnswerIndex - The index of the selected possible answer (1-based index).
         */
        selectAnswer(possibleAnswerIndex) {
            this.$emit('answer-selected', possibleAnswerIndex + 1);
        }
    },
}

</script>