<template>
    <Modal v-on:close="$emit('close')">
        <template v-if="schema">
            <p>Sort by:</p>

            <select
                name="property"
                v-model="propertyName"
            >
                <option value="id">id</option>

                <option
                    :key="key"
                    :value="key"
                    v-for="(property, key) in schema.properties"
                >{{ key }}</option>
            </select>

            <label>Ascending</label>
            <input
                name="ascending"
                type="radio"
                v-model="ascending"
                value="ascending"
            />

            <label>Descending</label>
            <input
                name="ascending"
                type="radio"
                v-model="ascending"
                value="descending"
            />

            <button v-on:click.prevent="save">Sort</button>
        </template>
    </Modal>
</template>

<script lang="ts">
import Modal from "./Modal.vue"
import * as i from "../interfaces"

export default {
    props: {
        schema: Object,
        tableName: String
    },
    data() {
        return {
            ascending: "descending",
            propertyName: "id"
        }
    },
    components: {
        Modal
    },
    methods: {
        async save() {
            let config: i.SortByConfig = {
                property: this.propertyName,
                ascending: this.ascending == "ascending"
            }
            this.$store.commit("updateSortBy", config)

            let filterParams = this.$store.state.filterParams

            let fetchRowsConfig: i.FetchRowsConfig = {
                tableName: this.tableName,
                params: filterParams
            }
            await this.$store.dispatch("fetchRows", fetchRowsConfig)

            this.$emit("close")
        }
    },
    mounted() {
        let sortBy: i.SortByConfig | null = this.$store.state.sortBy
        if (sortBy) {
            this.ascending = sortBy.ascending ? "ascending" : "descending"
            this.propertyName = sortBy.property
        }
    }
}
</script>

<style>
</style>
