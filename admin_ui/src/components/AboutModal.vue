<template>
    <Modal v-on:close="hideAboutModal">
        <h1>{{ $t("About") }}</h1>
        <p>{{ $t("Thanks for using Piccolo Admin.") }}</p>
        <p>{{ $t("Version") }} {{ piccoloAdminVersion }}</p>
    </Modal>
</template>

<script lang="ts">
import Modal from "./Modal.vue"

export default {
    components: {
        Modal
    },
    computed: {
        piccoloAdminVersion() {
            return this.$store.state.metaModule.piccoloAdminVersion
        }
    },
    methods: {
        hideAboutModal() {
            this.$store.commit("updateShowAboutModal", false)
        }
    }
}
</script>
