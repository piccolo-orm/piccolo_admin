<template>
    <div>
        <template v-for="(property, columnName) in schema.properties">
            <div
                v-bind:key="property.title"
                v-if="schema.visible_filter_names.includes(String(columnName))"
            >
                <template v-if="property.extra.foreign_key">
                    <label>
                        {{ property.title }}
                    </label>
                    <KeySearch
                        v-bind:fieldName="String(columnName)"
                        v-bind:isFilter="true"
                        v-bind:key="getValue(property.title)"
                        v-bind:readable="getValue(property.title)"
                        v-bind:rowID="getValue(property.title)"
                        v-bind:tableName="property.extra.to"
                        v-bind:isNullable="property.nullable"
                    />
                </template>
                <template v-else-if="property.format !== 'json'">
                    <label>
                        {{ property.title }}
                    </label>

                    <InputField
                        v-bind:columnName="columnName"
                        v-bind:choices="property.extra.choices"
                        v-bind:format="property.format"
                        v-bind:isFilter="true"
                        v-bind:isNullable="property.nullable"
                        v-bind:key="property.title"
                        v-bind:required="isRequired(String(columnName))"
                        v-bind:title="property.title"
                        v-bind:type="property.type || property.anyOf[0].type"
                        v-bind:value="getValue(String(columnName))"
                    />
                </template>
            </div>
        </template>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue"

import KeySearch from "./KeySearch.vue"
import InputField from "./InputField.vue"
import { Schema } from "@/interfaces"

export default Vue.extend({
    props: {
        row: Object,
        schema: Object as PropType<Schema>
    },
    components: {
        InputField,
        KeySearch
    },
    methods: {
        getValue(columnName: string) {
            return this.row ? this.row[columnName] : undefined
        },
        isRequired(keyName: string) {
            return (
                !this.isFilter &&
                (this.schema.required || []).indexOf(keyName) != -1
            )
        }
    }
})
</script>
