<template>
    <div class="modal" :id="id" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ titre }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>{{ body }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fermer</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="handleClickButtonOk" >Confirmer</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
/**
 * Component: ValidationModal
 * Description: Represents a validation modal with a title, body, and an OK button.
 *
 * Props:
 *   - titre: [String] The title of the validation modal.
 *   - body: [String] The body content of the validation modal.
 *   - id: [String] The unique ID of the validation modal. (Type: String, Default: "validation-modal")
 *
 * Methods:
 *   - handleClickButtonOk: Handles the click event on the OK button and emits a "modal-click-btn-ok" event.
 */
export default {
    name: "ValidationModal",
    props: {
        titre: String,
        body: String,
        id: {
            type: String,
            default: "validation-modal"
        }
    },
    methods:{
        /**
        * Handles the click event on the OK button and emits a "modal-click-btn-ok" event.
        */
        handleClickButtonOk(){
            this.$emit("modal-click-btn-ok");
        }
    }
}
</script>