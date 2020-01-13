<template>
    <select :name="fieldName + '__operator'">
        <option
            :key="operator.label"
            :selected="operator.value == 'e'"
            :value="operator.value"
            v-for="operator in operators"
        >{{ operator.label }}</option>
    </select>
</template>

<script>
export default {
    props: {
        fieldName: String
    },
    data() {
        return {
            operators: [
                {
                    label: "Less Than",
                    value: "lt"
                },
                {
                    label: "Less Than or Equal To",
                    value: "lte"
                },
                {
                    label: "Equals",
                    value: "e"
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
    }
}
</script>

<style>
</style>
