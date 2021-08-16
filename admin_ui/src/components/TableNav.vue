<template>
    <ul>
        <li
            v-bind:key="tableName"
            v-for="tableName in tableNames"
        >
            <router-link
                :to="{ name: 'rowListing', params: { tableName } }"
                class="subtle"
                v-bind:class="{active: isActive(tableName)}"
            >
                <font-awesome-icon icon="level-up-alt" />
                {{ readable(tableName) }}
            </router-link>
        </li>
    </ul>
</template>


<script lang="ts">
export default {
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
        readable(value) {
            return value.split("_").join(" ")
        },
    },
    async mounted() {
        await this.$store.dispatch("fetchTableNames")
    },
}
</script>


<style scoped lang="less">
ul {
    padding: 0;

    li {
        list-style: none;
        text-indent: 0.5rem;
        text-transform: capitalize;

        svg {
            transform: rotate(90deg);
        }
    }
}
</style>
