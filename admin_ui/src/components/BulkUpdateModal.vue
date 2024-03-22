<template>
    <Modal v-on:close="$emit('close')" title="Bulk Update">
        <template v-if="schema">
            <p>{{ $t("Select a column to update") }}</p>

            <select name="property" v-model="selectedPropertyName">
                <option value="null" disabled>
                    {{ $t("Select a Column") }}
                </option>
                <template v-for="(property, columnName) in schema.properties">
                    <option
                        :key="columnName"
                        :value="columnName"
                        v-if="
                            columnName != schema.extra.primary_key_name &&
                            property.extra.unique == false
                        "
                    >
                        {{ property.title }}
                    </option>
                </template>
            </select>

            <p v-show="selectedPropertyName">{{ $t("New value") }}</p>

            <form
                v-on:submit.prevent="updateRows($event)"
                v-if="selectedPropertyName && selectedProperty"
            >
                <KeySearch
                    v-bind:fieldName="selectedPropertyName"
                    v-bind:tableName="selectedProperty.extra.foreign_key.to"
                    v-bind:key="selectedProperty.title"
                    v-bind:isNullable="selectedProperty.extra.nullable"
                    v-if="selectedProperty.extra.foreign_key"
                />

                <InputField
                    v-bind:columnName="selectedPropertyName"
                    v-bind:format="getFormat(selectedProperty)"
                    v-bind:isFilter="false"
                    v-bind:type="
                        selectedProperty.type ||
                        selectedProperty.anyOf?.[0].type
                    "
                    v-bind:choices="selectedProperty.extra.choices"
                    v-bind:widget="selectedProperty.extra.widget"
                    v-bind:timeResolution="
                        schema?.extra?.time_resolution[selectedPropertyName]
                    "
                    v-else
                />

                <div class="set_null" v-if="selectedProperty.extra.nullable">
                    <label>Set null:</label>
                    <input type="checkbox" v-model="nullCheckboxState" />
                </div>

                <button :disabled="!buttonEnabled">{{ $t("Update") }}</button>
            </form>
        </template>
    </Modal>
</template>

<script lang="ts">
import { type PropType, defineComponent } from "vue"
import InputField from "../components/InputField.vue"
import KeySearch from "../components/KeySearch.vue"
import Modal from "../components/Modal.vue"
import {
    type Schema,
    type APIResponseMessage,
    getFormat,
    getType
} from "../interfaces"

export default defineComponent({
    props: {
        schema: Object as PropType<Schema>,
        tableName: String,
        selectedRows: {
            type: Array,
            default: () => []
        }
    },
    components: {
        Modal,
        InputField,
        KeySearch
    },
    data() {
        return {
            selectedPropertyName: null as string | null,
            nullCheckboxState: false,
            buttonEnabled: true
        }
    },
    computed: {
        selectedProperty() {
            return this.selectedPropertyName
                ? this.schema?.properties[this.selectedPropertyName]
                : undefined
        }
    },
    setup() {
        return {
            getFormat
        }
    },
    methods: {
        async updateRows(event: Event) {
            console.log("Updating ...")

            if (!this.selectedProperty || !this.selectedPropertyName) {
                return
            }

            // We prevent the button from being clicked again until we've
            // finished, as it can cause many API requests.
            this.buttonEnabled = false

            const form = new FormData(event.target as HTMLFormElement)

            const json: { [key: string]: any } = {}

            let value = null

            if (!this.nullCheckboxState) {
                value = form.get(this.selectedPropertyName)

                if (
                    getType(this.selectedProperty) == "array" &&
                    typeof value === "string"
                ) {
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
                var message: APIResponseMessage = {
                    contents: "Successfully updated rows",
                    type: "success"
                }
                this.$store.commit("updateApiResponseMessage", message)

                this.$emit("close")

                await this.$store.dispatch("fetchRows")
            } catch (error) {
                console.log(error)
                var message: APIResponseMessage = {
                    contents: "Invalid column name or value",
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)
            }

            this.buttonEnabled = true
        }
    }
})
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
