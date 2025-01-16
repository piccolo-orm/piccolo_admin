<template>
    <div>
        <template v-if="formConfig && !successMessage">
            <h1>{{ formConfig.name }}</h1>

            <p v-if="formConfig.description">
                {{ formConfig.description }}
            </p>
        </template>

        <div v-show="successMessage">
            <h1>{{ $t("Form submitted") }}</h1>
            <p id="success_message">{{ successMessage }}</p>
            <ul>
                <li>
                    <a href="#" @click.prevent="resetForm">{{
                        $t("Use again")
                    }}</a>
                </li>
                <li>
                    <router-link to="/">{{
                        $t("Back to home page")
                    }}</router-link>
                </li>
            </ul>
        </div>

        <div v-if="!successMessage">
            <FormErrors :errors="errors" v-if="errors.length > 0" />

            <form
                v-if="schema"
                v-on:submit.prevent="submitForm($event)"
                ref="form"
            >
                <NewForm :schema="schema" />
                <button data-uitest="submit_custom_form_button">
                    {{ $t("Submit") }}
                </button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import axios from "axios"
import { defineComponent, type PropType } from "vue"

import NewForm from "./NewForm.vue"
import type { APIResponseMessage, FormConfig, Schema } from "../interfaces"
import { convertFormValue, parseErrorResponse } from "@/utils"
import FormErrors from "./FormErrors.vue"

const BASE_URL = import.meta.env.VITE_APP_BASE_URI

// As we can potentially get a file as a response, we have to get it as a blob.
// This means we get an error, we have to convert the blob into JSON.
const convertBlobToJSON = async (
    blob: Blob
): Promise<{ [key: string]: string }> => {
    if (blob.type == "application/json") {
        return JSON.parse(await blob.text())
    }
    return {}
}

export default defineComponent({
    props: {
        formSlug: {
            type: String as PropType<string>,
            required: true
        },
        schema: {
            type: Object as PropType<Schema>,
            required: true
        }
    },
    components: {
        NewForm,
        FormErrors
    },
    data() {
        return {
            errors: [] as string[],
            formConfig: undefined as FormConfig | undefined,
            successMessage: null as string | null
        }
    },
    watch: {
        async formSlug() {
            await this.fetchFormConfig()
        }
    },
    methods: {
        resetForm() {
            this.successMessage = null
            this.errors = []
        },
        async fetchFormConfig() {
            const response = await this.$store.dispatch(
                "fetchFormConfig",
                this.formSlug
            )
            this.formConfig = response.data
        },
        async submitForm(event: any) {
            const form = new FormData(event.target)

            const json: { [key: string]: any } = {}
            for (const i of form.entries()) {
                const key = i[0]
                let value: any = i[1]

                json[key] = convertFormValue({
                    key,
                    value,
                    schema: this.schema
                })
            }

            try {
                var response = await axios.post(
                    `${BASE_URL}forms/${this.formSlug}/`,
                    json,
                    { responseType: "blob" }
                )
            } catch (error) {
                var message: APIResponseMessage = {
                    contents: "The form has errors.",
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)

                if (axios.isAxiosError(error) && error.response) {
                    const data = await convertBlobToJSON(error.response.data)

                    this.errors = parseErrorResponse(
                        data,
                        error.response.status
                    )
                }

                return
            }

            const contentDisposition = response.headers["content-disposition"]

            if (
                contentDisposition &&
                contentDisposition.startsWith("attachment")
            ) {
                // It's a file we need to download
                const fileName = contentDisposition
                    .split("filename=")[1]
                    .replaceAll('"', "")
                const url = window.URL.createObjectURL(
                    new Blob([response.data])
                )
                const link = document.createElement("a")
                link.href = url
                link.setAttribute("download", fileName)
                document.body.appendChild(link)
                link.click()

                this.successMessage = "Downloaded file"
            } else {
                const data = await convertBlobToJSON(response.data)

                this.successMessage =
                    data.custom_form_success || "Successfully submitted form"
            }

            this.errors = []
        }
    },
    async mounted() {
        await this.fetchFormConfig()
    }
})
</script>

<style scoped lang="less">
h1 {
    text-transform: capitalize;
}

p#success_message {
    white-space: pre-wrap;
}
</style>
