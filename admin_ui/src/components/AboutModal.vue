<template>
    <Modal v-on:close="hideAboutModal">
        <h1>About</h1>
        <p>Thanks for using Piccolo Admin.</p>
        <p>Version {{ meta.piccolo_admin_version }}</p>
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"

export default {
    components: {
        Modal
    },
    computed: {
        meta() {
            return this.$store.state.aboutModal.meta
        }
    },
    methods: {
        hideAboutModal() {
            this.$store.commit("updateShowAboutModal", false)
        }
    },
    async created() {
        await this.$store.dispatch("fetchMeta")
    }
}
</script>

<style>
</style>
