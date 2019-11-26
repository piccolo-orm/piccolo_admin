<template>
    <Modal v-on:close="$emit('close')">
        <h1>Add</h1>

        <form v-on:submit.prevent="submitForm($event)">
            <RowForm v-bind:schema="schema"/>
            <button>Create</button>
        </form>
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"
import RowForm from "./RowForm.vue"

export default {
    props: {
        tableName: String,
        schema: Object
    },
    components: {
        Modal,
        RowForm
    },
    methods: {
        async submitForm(event) {
            console.log("I was pressed")
            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                json[i[0]] = i[1]
            }
            const response = await this.$store.dispatch("createRow", {
                tableName: this.tableName,
                data: json
            })
            this.$emit("addedRow")
        }
    }
}
</script>

<style scoped lang="less">
</style>
