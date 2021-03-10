<template>
    <select
        v-bind:name="fieldName"
        v-model="selectedValue"
        v-on:change="$emit('valueChanged', selectedValue)"
    >
        <option v-if="isFilter" value="all">All</option>
        <option v-if="isNullable" value="null">Null</option>
        <option
            :key="id"
            :selected="value == id"
            :value="id"
            v-for="(readable, id) in ids"
        >
            {{ readable }}
        </option>
    </select>
</template>


<script lang="ts">
import { FetchIdsConfig } from "../interfaces"

export default {
    props: {
        fieldName: String,
        tableName: String,
        value: undefined,
        isFilter: {
            type: Boolean,
            default: false,
        },
        isNullable: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            ids: [],
            selectedValue: undefined,
        }
    },
    methods: {
        async fetchData() {
            const config: FetchIdsConfig = {
                tableName: this.tableName,
                search: undefined,
                limit: undefined,
            }
            const response = await this.$store.dispatch("fetchIds", config)
            this.ids = response.data
        },
    },
    watch: {
        async tableName() {
            await this.fetchData()
        },
        value() {
            this.selectedValue = this.value
        },
    },
    async mounted() {
        await this.fetchData()
        this.selectedValue = this.value
    },
}
</script>


<style>
</style>