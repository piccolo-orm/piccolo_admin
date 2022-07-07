<template>
    <Modal v-on:close="$emit('close')">
        <template v-if="schema">
            <p>Select a column to update</p>

            <select name="property" v-model="propertyName">
                <option
                    :key="key"
                    :value="key"
                    v-for="(property, key) in schema.properties"
                >
                    {{ key }}
                </option>
            </select>
            <p v-show="propertyName">Value to change</p>

            <form v-on:submit.prevent="updateRows($event)">
                <div :key="key" v-for="(property, key) in schema.properties">
                    <InputField
                        v-if="key == propertyName"
                        v-bind:format="property.format"
                        v-bind:isFilter="false"
                        v-bind:key="property.title"
                        v-bind:title="property.title"
                        v-bind:type="property.type || property.anyOf[0].type"
                        v-bind:choices="property.extra.choices"
                    />
                </div>
                <button>Update</button>
            </form>
        </template>
    </Modal>
</template>


<script lang="ts">
import InputField from "../components/InputField.vue"
import Modal from "../components/Modal.vue"
import * as i from "../interfaces"

export default {
    props: {
        schema: Object,
        tableName: String,
        selectedRows: {
            type: Array,
            defult: () => []
        }
    },
    components: {
        Modal,
        InputField
    },
    data() {
        return {
            propertyName: null
        }
    },
    methods: {
        async updateRows(event) {
            console.log("Updating ...")

            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                const key = i[0].split(" ").join("_")
                let value = i[1]

                if (value == "null") {
                    value = null
                } else if (this.schema.properties[key].type == "array") {
                    // @ts-ignore
                    value = JSON.parse(value)
                } else if (
                    this.schema?.properties[key].format == "date-time" &&
                    value == ""
                ) {
                    value = null
                } else if (
                    this.schema?.properties[key].extra.foreign_key == true &&
                    value == ""
                ) {
                    value = null
                }
                json[key] = value
            }

            for (let i = 0; i < this.selectedRows.length; i++) {
                await this.$store
                    .dispatch("updateRow", {
                        tableName: this.tableName,
                        rowID: this.selectedRows[i],
                        data: json
                    })
                    .then(() => {
                        var message: i.APIResponseMessage = {
                            contents: "Successfully updated rows",
                            type: "success"
                        }
                        this.$store.commit("updateApiResponseMessage", message)
                    })
                    .catch((error) => {
                        console.log(error)
                        var message: i.APIResponseMessage = {
                            contents: "Invalid column name or value",
                            type: "error"
                        }
                        this.$store.commit("updateApiResponseMessage", message)
                    })
            }
            this.$emit("close")
            await this.fetchRows()
        },
        async fetchRows() {
            await this.$store.dispatch("fetchRows")
        }
    }
}
</script> 