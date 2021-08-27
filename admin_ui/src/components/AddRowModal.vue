<template>
    <Modal v-on:close="$emit('close')">
        <AddRowForm
            v-bind:schema="schema"
            v-bind:tableName="tableName"
            v-on:addedRow="$emit('addedRow')"
            v-on:close="$emit('close')"
        />
    </Modal>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import Modal from "./Modal.vue"
import AddRowForm from "./AddRowForm.vue"

export default defineComponent({
    props: {
        tableName: String,
        schema: Object,
    },
    components: {
        Modal,
        AddRowForm,
    },
})
</script>

<style scoped lang="less">
</style>
