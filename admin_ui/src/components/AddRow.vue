<template>
    <Modal v-on:close="$emit('close')">
        <h1>Add</h1>

        <form v-on:submit.prevent="submitForm($event)">
            <InputField
                v-bind:format="property.format"
                v-bind:key="property.title"
                v-bind:title="property.title"
                v-bind:type="property.type"
                v-bind:value="undefined"
                v-for="property in schema.properties"
            />
            <button>Create</button>
        </form>
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"
import InputField from "./InputField.vue"

export default {
    props: {
        tableName: String,
        schema: Object
    },
    components: {
        InputField,
        Modal
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
