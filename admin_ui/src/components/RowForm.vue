<template>
<div>
    <div v-for="property in schema.properties" v-bind:key="property.title">
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
                v-bind:type="property.type || property.anyOf[0].type"
                v-bind:value="getValue(property.title)"
            />
        </template>
    </div>
</div>
</template>

<script>
import KeySelect from "./KeySelect.vue"
import InputField from "./InputField.vue"

export default {
    props: {
        row: Object,
        schema: Object,
    },
    components: {
        InputField,
        KeySelect
    },
    methods: {
        getValue(propertyTitle) {
            let value = this.row
                ? this.row[
                      propertyTitle.toLowerCase().replace(" ", "_")
                  ]
                : undefined
            return value
        },
    },
}
</script>

<style>

</style>
