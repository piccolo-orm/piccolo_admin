<template>
    <ul>
        <li
            v-bind:key="tableName"
            v-for="tableName in tableNames"
        >
            <a
                href="#"
                v-bind:class="{active: isActive(tableName)}"
                v-on:click.prevent="showListing(tableName)"
            >{{ tableName | readable }}</a>
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
        }
    },
    methods: {
        showListing(tableName: string) {
            this.$store.commit("updateCurrentTablename", tableName)
            this.$router.push({ name: "rowListing", params: { tableName } })
        },
        isActive(tableName: string): boolean {
            return this.currentTableName === tableName
        }
    },
    filters: {
        readable(value) {
            return value.split("_").join(" ")
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchTableNames")
    }
})
</script>


<style scoped lang="less">
ul {
    padding: 0;

    li {
        text-transform: capitalize;
        list-style: none;
    }
}
</style>
