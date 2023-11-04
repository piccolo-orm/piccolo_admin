<template>
    <Modal v-on:close="$emit('close')">
        <h1>{{ $t("About") }}</h1>
        <p>{{ $t("Thanks for using Piccolo Admin.") }}</p>
        <p>{{ $t("Version") }} {{ piccoloAdminVersion }}</p>
    </Modal>
</template>

<script lang="ts">
import { defineComponent } from "vue"

import Modal from "./Modal.vue"

export default defineComponent({
    components: {
        Modal
    },
    computed: {
        piccoloAdminVersion() {
            return this.$store.state.metaModule.piccoloAdminVersion
        }
    }
})
</script>
