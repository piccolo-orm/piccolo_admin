<template>
    <div>
        <h1>{{ $t("Add") }} {{ tableName | readable }}</h1>

        <FormErrors v-if="errors.length > 0" v-bind:errors="errors" />

        <form v-if="defaults" v-on:submit.prevent="submitForm($event)">
            <RowForm v-bind:row="defaults" v-bind:schema="schema" />
            <button>{{ $t("Create") }}</button>
        </form>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue"
import RowForm from "./RowForm.vue"
import FormErrors from "./FormErrors.vue"
import { APIResponseMessage } from "../interfaces"
import { parseErrorResponse } from "../utils"
import { Schema } from "@/interfaces"

export default Vue.extend({
    props: {
        tableName: String as PropType<string>,
        schema: Object as PropType<Schema>
    },
    components: {
        RowForm,
        FormErrors
    },
    data() {
        return {
            defaults: {} as { [key: string]: any },
            errors: [] as string[]
        }
    },
    methods: {
        async submitForm(event) {
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
                this.errors = parseErrorResponse(
                    error.response.data,
                    error.response.status
                )

                window.scrollTo(0, 0)

                var message: APIResponseMessage = {
                    contents: "The form has errors.",
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)

                return
            }
            this.errors = []

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
})
</script>

<style scoped lang="less">
h1 {
    text-transform: capitalize;
}
</style>
