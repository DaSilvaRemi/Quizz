<template>
    <div class="modal" id="validation-modal" tabindex="-1">
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
export default {
    name: "ValidationModal",
    props: {
        titre: String,
        body: String,
    },
    methods:{
        handleClickButtonOk(){
            this.$emit("modal-click-btn-ok");
        }
    }
}
</script>