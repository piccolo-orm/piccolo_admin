<template>
    <div>
        <h1>{{ $t("Add") }} {{ tableName | readable }}</h1>

        <RowFormErrors v-if="errors" v-bind:errors="errors" />

        <form v-if="defaults" v-on:submit.prevent="submitForm($event)">
            <RowFormSelect v-bind:row="defaults" v-bind:schema="schema" />
            <button>{{ $t("Create") }}</button>
        </form>
    </div>
</template>

<script lang="ts">
import RowFormSelect from "./RowFormSelect.vue"
import RowFormErrors from "./RowFormErrors.vue"
import { APIResponseMessage } from "../interfaces"
import { parseErrorResponse } from "../utils"

export default {
    props: {
        tableName: String,
        schema: Object
    },
    components: {
        RowFormSelect,
        RowFormErrors
    },
    data() {
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
                const key = i[0]
                let value = i[1]

                if (value == "null") {
                    value = null
                    // @ts-ignore
                } else if (this.schema.properties[key].type == "array") {
                    // @ts-ignore
                    value = JSON.parse(value)
                    // @ts-ignore
                } else if (
                    this.schema?.properties[key].format == "date-time" &&
                    value == ""
                ) {
                    value = null
                    // @ts-ignore
                } else if (
                    this.schema?.properties[key].extra.foreign_key == true &&
                    value == ""
                ) {
                    value = null
                }
                json[key] = value
            }
            try {
                await this.$store.dispatch("createRow", {
                    tableName: this.tableName,
                    data: json
                })
            } catch (error) {
                const data = error.response.data

                let errorsArray: string[] = []

                if (error.response.status == 422) {
                    this.errors = parseErrorResponse(data)
                } else if (error.response.status == 405) {
                    this.errors = data
                } else {
                    errorsArray.push(data)
                    this.errors = errorsArray
                }

                var message: APIResponseMessage = {
                    contents: "The form has errors.",
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)

                return
            }
            this.errors = ""

            var message: APIResponseMessage = {
                contents: "Successfully added row",
                type: "success"
            }
            this.$store.commit("updateApiResponseMessage", message)

            this.$emit("addedRow")
            this.$emit("close")
            if (opener) {
                opener.postMessage("edited row", document.location.origin)
            }
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
