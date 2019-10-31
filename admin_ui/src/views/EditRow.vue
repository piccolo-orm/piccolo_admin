<template>
    <div>
        <NavBar />
        <div
            class="edit_wrapper"
            v-if="schema"
        >
            <p>
                <a
                    href="#"
                    v-on:click.prevent="$router.go(-1)"
                >Back</a>
            </p>

            <h1>Edit</h1>

            <form v-on:submit.prevent="submitForm($event)">
                <div
                    v-bind:key="property.title"
                    v-for="property in schema.properties"
                >
                    <template v-if="property.foreign_key">
                        <label>{{ property.title }}</label>
                        <KeySelect
                            v-bind:fieldName="property.title.toLowerCase()"
                            v-bind:tableName="property.to"
                            v-bind:value="getValue(property.title)"
                        />
                    </template>
                    <template v-else>
                        <InputField
                            v-bind:format="property.format"
                            v-bind:key="property.title"
                            v-bind:title="property.title"
                            v-bind:type="property.type"
                            v-bind:value="getValue(property.title)"
                        />
                    </template>
                </div>
                <button>Save</button>
            </form>
        </div>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import InputField from "../components/InputField.vue"
import NavBar from "../components/NavBar.vue"
import KeySelect from "../components/KeySelect.vue"
import { UpdateRow } from "../interfaces"

export default Vue.extend({
    props: ["tableName", "rowID"],
    components: {
        InputField,
        NavBar,
        KeySelect
    },
    computed: {
        schema() {
            return this.$store.state.schema
        },
        selectedRow() {
            return this.$store.state.selectedRow
        }
    },
    methods: {
        getValue(propertyTitle) {
            let value = this.selectedRow
                ? this.selectedRow[
                      propertyTitle.toLowerCase().replace(" ", "_")
                  ]
                : ""
            return value
        },
        async submitForm(event) {
            console.log("Submitting...")

            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                json[i[0].replace(" ", "_")] = i[1]
            }

            let config: UpdateRow = {
                tableName: this.tableName,
                rowID: this.rowID,
                data: json
            }
            this.$store.dispatch("updateRow", config)
        }
    },
    async mounted() {
        this.$store.commit("updateCurrentTablename", this.tableName)
        await Promise.all([
            this.$store.dispatch("fetchSingleRow", {
                tableName: this.tableName,
                rowID: this.rowID
            }),
            this.$store.dispatch("fetchSchema", this.tableName)
        ])
    }
})
</script>


<style lang="less">
div.edit_wrapper {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;

    h1 {
        margin: 0;
    }
}
</style>
