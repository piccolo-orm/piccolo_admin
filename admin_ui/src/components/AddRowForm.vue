<template>
    <div>
        <h1>Add {{ tableName | readable }}</h1>

        <pre>{{ errors }}</pre>

        <form
            v-if="defaults"
            v-on:submit.prevent="submitForm($event)"
        >
            <RowFormSelect
                v-bind:row="defaults"
                v-bind:schema="schema"
            />
            <button>Create</button>
        </form>
    </div>
</template>

<script lang="ts">
import RowFormSelect from "./RowFormSelect.vue"
import { APIResponseMessage } from "../interfaces"

export default {
    props: {
        tableName: String,
        schema: Object,
    },
    components: {
        RowFormSelect,
    },
    data: function () {
        return {
            defaults: {},
            errors: "",
        }
    },
    methods: {
        async submitForm(event) {
            console.log("I was pressed")
            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                json[i[0].split(" ").join("_")] = i[1]
            }
            try {
                await this.$store.dispatch("createRow", {
                    tableName: this.tableName,
                    data: json,
                })
            } catch (error) {
                this.errors = error.response.data
                return
            }

            var message: APIResponseMessage = {
                contents: "Successfully added row",
                type: "success",
            }
            this.$store.commit("updateApiResponseMessage", message)

            this.$emit("addedRow")
            this.$emit("close")
            if (opener) {
                opener.postMessage("edited row", document.location.origin)
            }
        },
    },
    async mounted() {
        let response = await this.$store.dispatch("getNew", this.tableName)
        this.defaults = response.data
    },
}
</script>

<style scoped lang="less">
h1 {
    text-transform: capitalize;
}
</style>