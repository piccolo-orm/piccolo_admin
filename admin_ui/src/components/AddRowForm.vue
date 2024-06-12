<template>
    <div>
        <h1>{{ $t("Add") }} {{ readable(tableName) }}</h1>

        <FormErrors v-if="errors.length > 0" v-bind:errors="errors" />

        <form v-if="defaults" v-on:submit.prevent="submitForm($event)">
            <RowForm v-bind:row="defaults" v-bind:schema="schema" />
            <button :disabled="!saveButtonEnabled" data-uitest="create_button">
                {{ $t("Create") }}
            </button>
        </form>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"
import RowForm from "./RowForm.vue"
import FormErrors from "./FormErrors.vue"
import { parseErrorResponse } from "../utils"
import type { Schema, APIResponseMessage } from "@/interfaces"
import { convertFormValue, readable } from "@/utils"
import axios from "axios"

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
        RowForm,
        FormErrors
    },
    data() {
        return {
            defaults: {} as { [key: string]: any },
            errors: [] as string[],
            saveButtonEnabled: true
        }
    },
    setup() {
        return {
            readable
        }
    },
    methods: {
        async submitForm(event: Event) {
            this.saveButtonEnabled = false

            const form = new FormData(event.target as HTMLFormElement)

            const json: { [key: string]: any } = {}
            for (const i of form.entries()) {
                const key = i[0]
                let value = i[1]

                json[key] = convertFormValue({
                    key,
                    value,
                    schema: this.schema
                })
            }
            try {
                await this.$store.dispatch("createRow", {
                    tableName: this.tableName,
                    data: json
                })

                this.errors = []

                var message: APIResponseMessage = {
                    contents: "Successfully added row",
                    type: "success"
                }
                this.$store.commit("updateApiResponseMessage", message)

                this.$emit("addedRow")
                this.$emit("close")
            } catch (error) {
                if (axios.isAxiosError(error) && error.response) {
                    this.errors = parseErrorResponse(
                        error.response.data,
                        error.response.status
                    )
                }

                window.scrollTo(0, 0)

                var message: APIResponseMessage = {
                    contents: "The form has errors.",
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)
            }

            this.saveButtonEnabled = true
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
