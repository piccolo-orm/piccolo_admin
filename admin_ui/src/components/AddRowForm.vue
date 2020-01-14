<template>
    <div>
        <h1>Add {{ tableName }}</h1>

        <pre>{{ errors }}</pre>

        <form
            v-if="defaults"
            v-on:submit.prevent="submitForm($event)"
        >
            <RowForm
                v-bind:row="defaults"
                v-bind:schema="schema"
            />
            <button>Create</button>
        </form>
    </div>
</template>

<script lang="ts">
import RowForm from "./RowForm.vue"
import { APIResponseMessage } from "../interfaces"

export default {
    props: {
        tableName: String,
        schema: Object
    },
    components: {
        RowForm
    },
    data: function() {
        return {
            defaults: {},
            errors: ""
        }
    },
    methods: {
        async submitForm(event) {
            console.log("I was pressed")
            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                json[i[0]] = i[1]
            }
            try {
                const response = await this.$store.dispatch("createRow", {
                    tableName: this.tableName,
                    data: json
                })
            } catch (error) {
                this.errors = error.response.data
                return
            }

            var message: APIResponseMessage = {
                contents: "Successfully added row",
                type: "success"
            }
            this.$store.commit("updateApiResponseMessage", message)

            this.$emit("addedRow")
            this.$emit("close")
        }
    },
    async mounted() {
        let response = await this.$store.dispatch("getNew", this.tableName)
        this.defaults = response.data
    }
}
</script>

<style scoped lang="less">
h1 {
    text-transform: capitalize;
}
</style>