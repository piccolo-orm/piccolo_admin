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
                    label: "<",
                    value: "lt"
                },
                {
                    label: "<=",
                    value: "lte"
                },
                {
                    label: "==",
                    value: "e"
                },
                {
                    label: ">=",
                    value: "gte"
                },
                {
                    label: ">",
                    value: "gt"
                }
            ]
        }
    }
}
</script>

<style>
</style>
