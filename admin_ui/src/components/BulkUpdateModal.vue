<template>
    <Modal v-on:close="$emit('close')" title="Bulk Update">
        <template v-if="schema">
            <p>{{ $t("Select a column to update:") }}</p>

            <select name="property" v-model="selectedPropertyName">
                <option value="null" disabled>
                    {{ $t("Select a Column") }}
                </option>
                <template v-for="(property, key) in schema.properties">
                    <option
                        :key="key"
                        :value="key"
                        v-if="key != schema.primary_key_name"
                    >
                        {{ property.title }}
                    </option>
                </template>
            </select>

            <p v-show="selectedPropertyName">{{ $t("New value:") }}</p>

            <form
                v-on:submit.prevent="updateRows($event)"
                v-if="selectedPropertyName"
            >
                <KeySearch
                    v-bind:fieldName="selectedPropertyName"
                    v-bind:key="selectedProperty.title"
                    v-bind:tableName="selectedProperty.extra.to"
                    v-bind:isNullable="selectedProperty.nullable"
                    v-if="selectedProperty.extra.foreign_key"
                />

                <InputField
                    v-bind:format="selectedProperty.format"
                    v-bind:isFilter="false"
                    v-bind:title="selectedProperty.title"
                    v-bind:type="
                        selectedProperty.type || selectedProperty.anyOf[0].type
                    "
                    v-bind:choices="selectedProperty.extra.choices"
                    v-else
                />

                <div class="set_null" v-if="selectedProperty.nullable">
                    <label>Set null:</label>
                    <input type="checkbox" v-model="nullCheckboxState" />
                </div>

                <button :disabled="!buttonEnabled">{{ $t("Update") }}</button>
            </form>
        </template>
    </Modal>
</template>

<script lang="ts">
import InputField from "../components/InputField.vue"
import KeySearch from "../components/KeySearch.vue"
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
        InputField,
        KeySearch
    },
    data() {
        return {
            selectedPropertyName: null,
            nullCheckboxState: false,
            buttonEnabled: true
        }
    },
    computed: {
        selectedProperty() {
            return this.schema.properties[this.selectedPropertyName]
        }
    },
    methods: {
        async updateRows(event) {
            console.log("Updating ...")

            // We prevent the button from being clicked again until we've
            // finished, as it can cause many API requests.
            this.buttonEnabled = false

            const form = new FormData(event.target)

            const json = {}

            let value = null

            if (!this.nullCheckboxState) {
                value = form.get(this.selectedPropertyName)

                if (this.selectedProperty.type == "array") {
                    value = JSON.parse(value)
                }
            }

            json[this.selectedPropertyName] = value

            try {
                // TODO - we will use the new bulk update endpoint once it is
                // merged into PiccoloCRUD.
                for (let i = 0; i < this.selectedRows.length; i++) {
                    await this.$store.dispatch("updateRow", {
                        tableName: this.tableName,
                        rowID: this.selectedRows[i],
                        data: json
                    })
                }
                var message: i.APIResponseMessage = {
                    contents: "Successfully updated rows",
                    type: "success"
                }
                this.$store.commit("updateApiResponseMessage", message)

                this.$emit("close")

                await this.$store.dispatch("fetchRows")
            } catch (error) {
                console.log(error)
                var message: i.APIResponseMessage = {
                    contents: "Invalid column name or value",
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)
            }

            this.buttonEnabled = true
        }
    }
}
</script>

<style lang="less">
div.set_null {
    display: flex;
    flex-direction: row;
    align-items: baseline;

    label {
        flex-grow: 1;
    }

    input {
        width: auto !important;
    }
}
</style>
