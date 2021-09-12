<template>
    <div>
        <h1>{{ formName | readable }}</h1>

        <pre>{{ errors }}</pre>

        <form
            v-if="defaults"
            v-on:submit.prevent="submitForm($event)"
        >
            <NewForm v-bind:schema="defaults" />
            <button>Submit</button>
        </form>
    </div>
</template>

<script lang="ts">
import axios from "axios"
import Vue from "vue"
import NewForm from "./NewForm.vue"
import { APIResponseMessage } from "../interfaces"

const BASE_URL = process.env.VUE_APP_BASE_URI

export default Vue.extend({
    props: {
        formName: String,
        schema: Object,
    },
    components: {
        NewForm,
    },
    data() {
        return {
            defaults: {},
            errors: "",
            formData: {},
        }
    },
    methods: {
        async submitForm(event: any) {
            console.log("I was pressed")
            const form = new FormData(event.target)

            const json = {} as any
            for (const i of form.entries()) {
                const key = i[0].split(" ").join("_")
                let value: any = i[1]

                if (value == "null") {
                    value = null
                    // @ts-ignore
                } else if (this.schema.properties[key].type == "array") {
                    value = JSON.parse(value)
                }
                json[key] = value
            }
            axios
                .post(`${BASE_URL}forms/${this.formName}/`, json)
                .then((res) => {
                    this.formData = res.data
                    this.$router.push("/")
                })
                .catch((error) => {
                    const data = error.response.data

                    if (typeof data != "string") {
                        this.errors = JSON.stringify(data, null, 2)
                    } else {
                        this.errors = data
                    }
                    return
                })
            this.errors = ""

            var message: APIResponseMessage = {
                contents: "Successfully posted form data",
                type: "success",
            }
            this.$store.commit("updateApiResponseMessage", message)

            this.$emit("close")
        },
    },
    async mounted() {
        let response = await this.$store.dispatch("getNewForm", this.formName)
        this.defaults = response.data
    },
})
</script>

<style scoped lang="less">
h1 {
    text-transform: capitalize;
}
</style>