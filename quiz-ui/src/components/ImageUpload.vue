<template>
    <input class="form-control" type="file" name="uploadInput" :disabled="isSaving || readOnly"
        accept="image/jpeg, image/png, image/gif" ref="fileInput" @change="handleChangeFile" required />
    <button class="btn" v-if="file && !readOnly" @click="handleClickRemoveImage"><i
            class="bi bi-x-circle-fill"></i></button>
</template>
<script>
/**
 * Component: ImageUpload
 * Description: A component for uploading and displaying images.
 *
 * Props:
 *   - image: [String] The URL or base64 data of the image to display. Default: ""
 *   - readOnly: [Boolean] Determines if the input is disabled or not. Default: false
 *
 * Events:
 *   - file-change: Triggered when a file is selected or removed. Emits the file data URL as a string.
 */

export default {
    name: "ImageUpload",
    emits: ["file-change"],
    props: {
        image: {
            type: String,
            default: ""
        },
        readOnly: {
            type: Boolean,
            default: false
        }
    },
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
    beforeUpdate() {
        if (this.image) {
            this.file = this.base64ImgtoFile(this.image, "monImage");

            const DATA_TRANSFER = new DataTransfer();
            DATA_TRANSFER.items.add(this.file);
            this.$refs.fileInput.files = DATA_TRANSFER.files;
        }
    },
    methods: {
        /**
         * Handles the file change event and reads the file asynchronously.
         * @param {Event} event - The file change event.
         */
        handleChangeFile(event) {
            this.isSaving = true;
            this.file = event.target.files[0];
            this.fileReader.readAsDataURL(this.file);
        },
        /**
        * Handles the click event to remove the image and emits an empty string for file change.
        */
        handleClickRemoveImage() {
            this.file = null;
            this.$emit("file-change", "");

            if (this.fileInput) {
                this.fileInput.value = "";
            }
        },
        /**
        * Converts a base64 string to a File object.
        * @param {String} base64String - The base64 string representing the image.
        * @param {String} filename - The name of the file.
        * @returns {File} - The converted File object.
        */
        base64ImgtoFile(base64String, filename) {
            const BASE_64_STRING_SPLITED = base64String.split(',');

            const MIME = BASE_64_STRING_SPLITED[0].match(/:(.*?);/)[1];
            const BASE64_STRING_SPLITED_DECODED = atob(BASE_64_STRING_SPLITED[BASE_64_STRING_SPLITED.length - 1]);

            let base64StringSplitedDecodedLength = BASE64_STRING_SPLITED_DECODED.length;
            const U_INT_8_ARRAY = new Uint8Array(base64StringSplitedDecodedLength);

            while (base64StringSplitedDecodedLength--) {
                U_INT_8_ARRAY[base64StringSplitedDecodedLength] = BASE64_STRING_SPLITED_DECODED.charCodeAt(base64StringSplitedDecodedLength);
            }

            return new File([U_INT_8_ARRAY], filename, { type: MIME });
        }

    }
};
</script>