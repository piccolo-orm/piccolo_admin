<template>
    <Modal v-on:close="hideAboutModal">
        <h1>About</h1>
        <p>Thanks for using Piccolo Admin.</p>
        <p>Version {{ piccoloAdminVersion }}</p>
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"

export default {
    components: {
        Modal,
    },
    computed: {
        piccoloAdminVersion() {
            return this.$store.state.metaModule.piccoloAdminVersion
        },
    },
    methods: {
        hideAboutModal() {
            this.$store.commit("updateShowAboutModal", false)
        },
    },
}
</script>

<style>
</style>
