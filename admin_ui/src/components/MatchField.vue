<template>
    <select :name="columnName + '__match'" v-model="selectedMatch">
        <option :key="match" :value="match" v-for="match in matches">
            {{ match }}
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
            selectedMatch: "contains", // default
            matches: ["contains", "exact", "starts", "ends"]
        }
    },
    mounted() {
        // read query params from url
        const queryValue = this.$route.query[
            this.columnName + "__match"
        ] as string

        // use match if present in query params, otherwise keep default
        if (queryValue && this.matches.includes(queryValue)) {
            this.selectedMatch = queryValue
        }
    }
})
</script>

<style>
select {
    text-transform: capitalize;
}
</style>
