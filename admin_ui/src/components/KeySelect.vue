<template>
<select v-bind:name="fieldName">
    <option value="null">----</option>
    <option
        v-for="(readable, id) in ids"
        v-bind:key="id"
        v-bind:value="id"
        v-bind:selected="value == id">{{ readable }}</option>
</select>
</template>


<script>
export default {
    props: [
        'fieldName',
        'tableName',
        'value'
    ],
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
