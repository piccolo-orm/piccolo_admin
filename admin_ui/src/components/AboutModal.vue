<template>
    <Modal v-on:close="hideAboutModal">
        <h1>About</h1>
        <p>Thanks for using Piccolo Admin.</p>
        <p>Version {{ piccoloAdminVersion }}</p>
    </Modal>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import Modal from "./Modal.vue"

export default defineComponent({
    components: {
        Modal,
    },
    computed: {
        piccoloAdminVersion() {
            return this.$store.state.piccoloAdminVersion
        },
    },
    methods: {
        hideAboutModal() {
            this.$store.commit("updateShowAboutModal", false)
        },
    },
})
</script>

<style>
</style>
