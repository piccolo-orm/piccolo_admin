<template>
    <select :name="columnName + '__operator'" v-model="selectedOperator">
        <option
            v-for="operator in operators"
            :key="operator.value"
            :value="operator.value"
        >
            {{ operator.label }}
        </option>
    </select>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

export default defineComponent({
    props: {
        columnName: {
            type: String as PropType<string>,
            required: true
        }
    },
    data() {
        return {
            selectedOperator: "e", // default
            operators: [
                {
                    label: "Equals",
                    value: "e"
                },
                {
                    label: "Not Equal",
                    value: "ne"
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
    mounted() {
        // read query params from url
        const queryValue = this.$route.query[
            this.columnName + "__operator"
        ] as string

        // use operator if present in query params otherwise keep default
        if (
            queryValue &&
            this.operators.some(
                (operator: any) => operator.value === queryValue
            )
        ) {
            this.selectedOperator = queryValue
        }
    }
})
</script>

<style></style>