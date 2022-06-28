<template>
    <div>
        <template v-if="formConfig">
            <h1>{{ formConfig.name }}</h1>

            <p v-if="formConfig.description">{{ formConfig.description }}</p>
        </template>

        <div v-show="successMessage">
            <p>{{ successMessage }}</p>
            <ul>
                <li>
                    <a href="#" @click.prevent="resetForm">Use again</a>
                </li>
                <li>
                    <router-link to="/">Back to home page</router-link>
                </li>
            </ul>
        </div>

        <div v-show="!successMessage">
            <pre>{{ errors }}</pre>

            <form
                v-if="schema"
                v-on:submit.prevent="submitForm($event)"
                ref="form"
            >
                <NewForm :schema="schema" />
                <button>Submit</button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import axios from "axios"
import Vue from "vue"
import NewForm from "./NewForm.vue"
import { APIResponseMessage, FormConfig } from "../interfaces"

const BASE_URL = process.env.VUE_APP_BASE_URI

export default Vue.extend({
    props: {
        formSlug: String,
        schema: Object
    },
    components: {
        NewForm
    },
    data() {
        return {
            errors: "",
            formConfig: undefined as FormConfig,
            successMessage: null
        }
    },
    watch: {
        async formSlug() {
            await this.fetchFormConfig()
        }
    },
    methods: {
        resetForm() {
            this.$refs.form.reset()
            this.successMessage = null
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

            const json = {}
            for (const i of form.entries()) {
                const key = i[0].split(" ").join("_")
                let value: any = i[1]

                if (value == "null") {
                    value = null
                } else if (this.schema.properties[key].type == "array") {
                    value = JSON.parse(value)
                }
                json[key] = value
            }

            try {
                var response = await axios.post(
                    `${BASE_URL}forms/${this.formSlug}/`,
                    json
                )
            } catch (error) {
                const data = error.response.data
                var message: APIResponseMessage = {
                    contents: "The form has errors.",
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)

                if (typeof data != "string") {
                    this.errors = JSON.stringify(data, null, 2)
                } else {
                    this.errors = data
                }
                return
            }

            this.successMessage =
                response.data.message || "Successfully submitted form"
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
</style>
