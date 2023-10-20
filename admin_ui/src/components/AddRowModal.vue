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
import { defineComponent, type PropType } from "vue"

import Modal from "./Modal.vue"
import AddRowForm from "./AddRowForm.vue"
import type { Schema } from "@/interfaces"

export default defineComponent({
    props: {
        tableName: {
            type: String as PropType<string>,
            required: true
        },
        schema: {
            type: Object as PropType<Schema>,
            required: true
        }
    },
    components: {
        Modal,
        AddRowForm
    }
})
</script>

<style scoped lang="less"></style>
