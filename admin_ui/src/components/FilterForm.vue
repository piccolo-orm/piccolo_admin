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
                <template v-else-if="getFormat(property) !== 'json'">
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

<script setup lang="ts">
import { type PropType, toRef } from "vue"

import InputField from "./InputField.vue"
import KeySearch from "./KeySearch.vue"
import { type Schema, getFormat, getType } from "@/interfaces"

/*****************************************************************************/

const props = defineProps({
    schema: {
        type: Object as PropType<Schema>,
        required: true
    }
})

const schema = toRef(props, "schema")

/*****************************************************************************/

const getValue = (columnName: string) => {
    if (getType(schema.value.properties[columnName]) == "boolean") {
        return "all"
    } else {
        return null
    }
}
</script>
