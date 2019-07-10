<template>
<ul>
    <li v-for="tableName in tableNames" v-bind:key="tableName">
        <a
            href="#"
            v-on:click.prevent="showListing(tableName)"
            v-bind:class="{active: isActive(tableName)}">{{ tableName }}</a>
    </li>
</ul>
</template>


<script lang="ts">
import Vue from 'vue';

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
            this.$store.commit('updateCurrentTablename', tableName)
            this.$router.push({name: 'rowListing', params: {tableName}})
        },
        isActive(tableName: string): boolean {
            return this.currentTableName === tableName
        }
    },
    async mounted() {
        await this.$store.dispatch('fetchTableNames')
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
