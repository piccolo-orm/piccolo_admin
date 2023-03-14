<template>
    <Modal v-on:close="$emit('close')">
        <template v-if="schema">
            <p>{{ $t("Sort by") }}:</p>

            <select
                name="property"
                v-model="propertyName"
                data-uitest="sort_by_selector"
            >
                <option :value="schema.primary_key_name">
                    {{ schema.primary_key_name }}
                </option>

                <option
                    :key="key"
                    :value="key"
                    v-for="(property, key) in schema.properties"
                >
                    {{ key }}
                </option>
            </select>

            <select name="ordering" v-model="ascending">
                <option value="ascending">{{ $t("Ascending") }}</option>
                <option value="descending">{{ $t("Descending") }}</option>
            </select>

            <button v-on:click.prevent="save">{{ $t("Sort") }}</button>
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
            propertyName: this.schema.sort_column_name
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

            await this.$store.dispatch("fetchRows")

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

<style></style>
