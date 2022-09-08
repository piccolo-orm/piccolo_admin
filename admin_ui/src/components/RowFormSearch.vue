<template>
    <div>
        <template v-for="(property, keyName) in schema.properties">
            <div
                v-bind:key="property.title"
                v-if="schema.visible_filter_names.includes(keyName)"
            >
                <template v-if="property.extra.foreign_key">
                    <label>
                        {{ property.title }}
                    </label>
                    <KeySearch
                        v-bind:fieldName="property.title.toLowerCase()"
                        v-bind:isFilter="true"
                        v-bind:key="getValue(property.title)"
                        v-bind:readable="getValue(property.title)"
                        v-bind:rowID="getKeySelectID(property.title)"
                        v-bind:tableName="property.extra.to"
                        v-bind:isNullable="property.nullable"
                    />
                </template>
                <template v-else-if="property.format !== 'json'">
                    <label>
                        {{ property.title }}
                    </label>

                    <InputField
                        v-bind:choices="property.extra.choices"
                        v-bind:format="property.format"
                        v-bind:isFilter="true"
                        v-bind:isNullable="property.nullable"
                        v-bind:key="property.title"
                        v-bind:required="isRequired(keyName)"
                        v-bind:title="property.title"
                        v-bind:type="property.type || property.anyOf[0].type"
                        v-bind:value="getValue(property.title)"
                    />
                </template>
            </div>
        </template>
    </div>
</template>

<script lang="ts">
import Vue, {PropType} from "vue"

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
        getValue(propertyTitle: string) {
            let value = this.row
                ? this.row[propertyTitle.toLowerCase().split(" ").join("_")]
                : undefined
            return value
        },
        getKeySelectID(propertyTitle: string) {
            return this.getValue(propertyTitle)
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
