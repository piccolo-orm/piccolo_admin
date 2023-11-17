<template>
    <select :name="columnName + '__match'">
        <option
            :key="match"
            :selected="match == 'contains'"
            :value="match"
            v-for="match in matches"
        >
            {{ match }}
        </option>
    </select>
</template>

<script setup lang="ts">
import type { PropType } from "vue"

defineProps({
    columnName: {
        type: String as PropType<string>,
        required: true
    }
})

const matches: string[] = ["contains", "exact", "starts", "ends"]
</script>

<style>
select {
    text-transform: capitalize;
}
</style>
