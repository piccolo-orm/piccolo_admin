<template>
    <div>
        <template v-for="(property, columnName) in schema.properties">
            <div
                v-bind:key="property.title"
                v-if="
                    schema.extra.visible_filter_names.includes(
                        String(columnName)
                    )
                "
            >
                <template v-if="property.extra.foreign_key">
                    <label>
                        {{ property.title }}
                    </label>
                    <KeySearch
                        v-bind:fieldName="String(columnName)"
                        v-bind:isFilter="true"
                        v-bind:key="property.title"
                        v-bind:tableName="property.extra.foreign_key.to"
                        v-bind:isNullable="property.extra.nullable"
                    />
                </template>
                <template v-else-if="property.format !== 'json'">
                    <label>
                        {{ property.title }}
                    </label>

                    <InputField
                        v-bind:columnName="String(columnName)"
                        v-bind:choices="property.extra.choices"
                        v-bind:format="getFormat(property)"
                        v-bind:isFilter="true"
                        v-bind:isNullable="property.extra.nullable"
                        v-bind:key="property.title"
                        v-bind:title="property.title"
                        v-bind:type="getType(property)"
                        v-bind:value="getValue(String(columnName))"
                        v-bind:widget="property.extra.widget"
                        v-bind:timeResolution="
                            schema?.extra?.time_resolution[columnName]
                        "
                    />
                </template>
            </div>
        </template>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

import KeySearch from "./KeySearch.vue"
import InputField from "./InputField.vue"
import { type Schema, getFormat, getType } from "@/interfaces"

export default defineComponent({
    props: {
        schema: {
            type: Object as PropType<Schema>,
            required: true
        }
    },
    components: {
        InputField,
        KeySearch
    },
    setup() {
        return {
            getFormat,
            getType
        }
    },
    methods: {
        getValue(columnName: string) {
            if (
                (this.schema as Schema).properties[columnName].type == "boolean"
            ) {
                return "all"
            } else {
                return null
            }
        }
    }
})
</script>
