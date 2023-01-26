<template>
    <div>
        <ul class="table_list">
            <TableNavItem
                v-bind:key="tableName"
                v-for="tableName in tableGroups.ungrouped"
                :tableName="tableName"
            />

            <template v-for="(tableNames, groupName) in tableGroups.grouped">
                <li class="group">
                    <a
                        href="#"
                        class="subtle"
                        @click.prevent="toggleGroup(groupName)"
                    >
                        <font-awesome-icon icon="layer-group" />
                        <span>{{ groupName }}</span>
                    </a>
                </li>

                <template v-if="hiddenGroups.indexOf(groupName) == -1">
                    <TableNavItem
                        v-bind:key="tableName"
                        v-for="tableName in tableNames"
                        :tableName="tableName"
                    />
                </template>
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
    data() {
        return { hiddenGroups: [] }
    },
    computed: {
        tableGroups() {
            return this.$store.state.tableGroups
        },
        currentTableName() {
            return this.$store.state.currentTableName
        }
    },
    methods: {
        toggleGroup(groupName: string) {
            const hiddenGroups: string[] = this.hiddenGroups
            const index = hiddenGroups.indexOf(groupName)
            if (index == -1) {
                hiddenGroups.push(groupName)
            } else {
                hiddenGroups.splice(index, 1)
            }
            this.hiddenGroups = hiddenGroups
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchTableGroups")
    }
})
</script>

<style scoped lang="less">
li.group {
    font-size: 0.7em;

    a {
        text-transform: uppercase;

        span {
            padding-left: 0;
        }
    }
}
</style>
