<template>
<select v-bind:name="fieldName">
    <option
        v-for="_value in ids"
        v-bind:key="_value"
        v-bind:value="_value"
        v-bind:selected="value === _value">{{ _value }}</option>
</select>
</template>


<script>
export default {
    props: {
        fieldName: String,
        tableName: String,
        value: Number
    },
    data() {
        return {
            ids: []
        }
    },
    async mounted() {
        const response = await this.$store.dispatch('fetchIds', this.tableName)
        this.ids = response.data
    }
}
</script>


<style>

</style>
