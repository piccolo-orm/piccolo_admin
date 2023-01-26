<template>
    <div>
        <ul class="table_list">
            <TableNavItem
                v-bind:key="tableName"
                v-for="tableName in tableGroups.ungrouped"
                :tableName="tableName"
            />

            <template
                v-for="(tableNames, tableGroupName) in tableGroups.grouped"
            >
                <li class="group">
                    <font-awesome-icon icon="layer-group" />
                    <span>{{ tableGroupName }}</span>
                </li>

                <TableNavItem
                    v-bind:key="tableName"
                    v-for="tableName in tableNames"
                    :tableName="tableName"
                />
            </template>
        </ul>
    </div>
</template>

<script lang="ts">
import Vue from "vue"
import TableNavItem from "./TableNavItem.vue"

export default Vue.extend({
    components: {
        TableNavItem
    },
    computed: {
        tableGroups() {
            return this.$store.state.tableGroups
        },
        currentTableName() {
            return this.$store.state.currentTableName
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchTableGroups")
    }
})
</script>

<style scoped lang="less">
li.group {
    padding: 0.5rem;
    text-transform: uppercase;
    font-size: 0.7em;
}
</style>
