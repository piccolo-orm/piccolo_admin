<template>
    <select :name="fieldName + '__operator'">
        <option
            :key="operator.label"
            :selected="operator.value == 'e'"
            :value="operator.value"
            v-for="operator in operators"
        >
            {{ operator.label }}
        </option>
        <option v-if="isNullable(fieldName)" value="null">Null</option>
    </select>
</template>

<script lang="ts">
export default {
    props: {
        fieldName: String
    },
    data() {
        return {
            operators: [
                {
                    label: "Equals",
                    value: "e"
                },
                {
                    label: "Less Than",
                    value: "lt"
                },
                {
                    label: "Less Than or Equal To",
                    value: "lte"
                },
                {
                    label: "Greater Than or Equal To",
                    value: "gte"
                },
                {
                    label: "Greater Than",
                    value: "gt"
                }
            ]
        }
    },
    computed: {
        schema() {
            return this.$store.state.schema
        }
    },
    methods: {
        isNullable(name: string) {
            let property = this.schema.properties[name]
            return property != undefined ? property.nullable : false
        }
    }
}
</script>

<style>
</style>
