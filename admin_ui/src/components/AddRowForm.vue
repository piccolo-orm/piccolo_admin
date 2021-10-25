<template>
    <div>
        <h1>Add {{ readable(tableName) }}</h1>

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
import { defineComponent } from "vue"
import RowFormSelect from "./RowFormSelect.vue"
import { APIResponseMessage } from "../interfaces"

export default defineComponent({
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
                    data: json,
                })
            } catch (error) {
                const data = error.response.data

                var message: APIResponseMessage = {
                    contents: "The form has errors.",
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
        readable(value: string) {
            return value.split("_").join(" ")
        },
    },
    async mounted() {
        let response = await this.$store.dispatch("getNew", this.tableName)
        this.defaults = response.data
    },
})
</script>

<style scoped lang="less">
h1 {
    text-transform: capitalize;
}
</style>