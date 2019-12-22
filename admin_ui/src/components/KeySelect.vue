<template>
<select v-bind:name="fieldName">
    <option value="all" v-if="isFilter">All</option>
    <option value="null" v-if="isNullable">Null</option>
    <option
        v-for="(readable, id) in ids"
        v-bind:key="id"
        v-bind:value="id"
        v-bind:selected="value == id">{{ readable }}</option>
</select>
</template>


<script>
export default {
    props: {
        'fieldName': String,
        'tableName': String,
        'value': undefined,
        'isFilter': {
            type: Boolean,
            default: false
        },
        'isNullable': {
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
        const response = await this.$store.dispatch('fetchIds', this.tableName)
        this.ids = response.data
    }
}
</script>


<style>

</style>
