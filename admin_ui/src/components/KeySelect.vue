<template>
    <select v-bind:name="fieldName">
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
            ids: []
        }
    },
    async mounted() {
        const response = await this.$store.dispatch("fetchIds", this.tableName)
        this.ids = response.data
    }
}
</script>


<style>
</style>
