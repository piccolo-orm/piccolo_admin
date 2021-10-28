<template>
    <ul class="table_list">
        <li v-bind:key="tableName" v-for="tableName in tableNames">
            <router-link
                :to="{ name: 'rowListing', params: { tableName } }"
                class="subtle"
                v-bind:class="{ active: isActive(tableName) }"
            >
                <font-awesome-icon icon="level-up-alt" />
                <span>{{ tableName | readable }}</span>
            </router-link>
        </li>
    </ul>
</template>


<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    computed: {
        tableNames() {
            return this.$store.state.tableNames
        },
        currentTableName() {
            return this.$store.state.currentTableName
        },
    },
    methods: {
        showListing(tableName: string) {
            this.$store.commit("updateCurrentTablename", tableName)
            this.$router.push({ name: "rowListing", params: { tableName } })
        },
        isActive(tableName: string): boolean {
            return this.currentTableName === tableName
        },
    },
    filters: {
        readable(value) {
            return value.split("_").join(" ")
        },
    },
    async mounted() {
        await this.$store.dispatch("fetchTableNames")
    },
})
</script>
