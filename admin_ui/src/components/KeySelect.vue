<template>
    <select
        v-bind:name="fieldName"
        v-model="selectedValue"
        v-on:change="$emit('valueChanged', selectedValue)"
    >
        <option
            v-if="isFilter"
            value="all"
        >All</option>
        <option
            v-if="isNullable"
            value="null"
        >Null</option>
        <option
            :key="id"
            :selected="value == id"
            :value="id"
            v-for="(readable, id) in ids"
        >{{ readable }}</option>
    </select>
</template>


<script>
export default {
    props: {
        fieldName: String,
        tableName: String,
        value: undefined,
        isFilter: {
            type: Boolean,
            default: false
        },
        isNullable: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            ids: [],
            selectedValue: undefined
        }
    },
    async mounted() {
        const response = await this.$store.dispatch("fetchIds", this.tableName)
        this.ids = response.data
        this.selectedValue = this.value
    }
}
</script>


<style>
</style>
