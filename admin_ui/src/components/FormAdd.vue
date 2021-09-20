<template>
    <div>
        <template v-if="formConfig">
            <h1>{{ formConfig.name }}</h1>

            <p v-if="formConfig.description">{{ formConfig.description }}</p>
        </template>

        <pre>{{ errors }}</pre>

        <form v-if="schema" v-on:submit.prevent="submitForm($event)">
            <NewForm :schema="schema" />
            <button>Submit</button>
        </form>
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
        schema: Object,
    },
    components: {
        NewForm,
    },
    data() {
        return {
            errors: "",
            formData: {},
            formConfig: undefined as FormConfig,
        }
    },
    watch: {
        async formSlug() {
            await this.fetchFormConfig()
        },
    },
    methods: {
        async fetchFormConfig() {
            const response = await this.$store.dispatch(
                "fetchFormConfig",
                this.formSlug
            )
            this.formConfig = response.data
        },
        async submitForm(event: any) {
            console.log("I was pressed")
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
                let response = await axios.post(
                    `${BASE_URL}forms/${this.formSlug}/`,
                    json
                )
                this.formData = response.data
                this.$router.push("/")
            } catch (error) {
                const data = error.response.data
                var message: APIResponseMessage = {
                    contents: "Errors in form",
                    type: "error",
                }
                this.$store.commit("updateApiResponseMessage", message)

                if (typeof data != "string") {
                    this.errors = JSON.stringify(data, null, 2)
                } else {
                    this.errors = data
                }
                return
            }

            this.errors = ""

            var message: APIResponseMessage = {
                contents: "Successfully posted form data",
                type: "success",
            }
            this.$store.commit("updateApiResponseMessage", message)
        },
    },
    async mounted() {
        await this.fetchFormConfig()
    },
})
</script>

<style scoped lang="less">
h1 {
    text-transform: capitalize;
}
</style>
