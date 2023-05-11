<template>
    <label class="form-label" for="image">Image</label>
    <input class="form-control" type="file" name="uploadInput" :disabled="isSaving" 
        accept="image/jpeg, image/png, image/gif" ref="fileInput" @change="handleChangeFile" required/>
    <button class="btn" v-if="file" @click="handleClickRemoveImage"><i class="bi bi-x-circle-fill"></i></button>
</template>
<script>
export default {
    name: "ImageUpload",
    emits: ["file-change"],
    data() {
        return {
            isSaving: false,
            fileReader: null,
            fileInput: null,
            file: null
        };
    },
    mounted() {
        this.fileInput = this.$refs.fileInput;
        this.fileReader = new FileReader();
        this.fileReader.addEventListener(
            "load",
            () => {
                // fileReader holds a b64 string of the image
                const fileDataUrl = this.fileReader?.result;
                this.isSaving = false;
                this.$emit("file-change", fileDataUrl);
            },
            false
        );
    },
    methods: {
        handleChangeFile(event) {
            this.isSaving = true;
            // pick the first file uploaded
            this.file = event.target.files[0];
            // feed the file to the asynchronous file reader
            // (next step is in the load eventListener defined in mounted)
            this.fileReader.readAsDataURL(this.file);
        },
        handleClickRemoveImage() {
            this.file = null;
            this.$emit("file-change", "");

            if (this.fileInput) {
                this.fileInput.value = "";
            }
        }
    }
};
</script>