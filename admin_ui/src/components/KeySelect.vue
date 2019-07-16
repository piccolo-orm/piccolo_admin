<template>
<select v-bind:name="fieldName">
    <option
        v-for="value in ids"
        v-bind:key="value"
        v-bind:value="value">{{ value }}</option>
</select>
</template>


<script>
export default {
    props: {
        fieldName: String,
        tableName: String
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
