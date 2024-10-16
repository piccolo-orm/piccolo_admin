<template>
    <div>
        <ul class="table_list">
            <TableNavItem
                v-bind:key="tableName"
                v-for="tableName in tableGroups.ungrouped"
                :tableName="tableName"
            />

            <template v-for="(tableNames, groupName) in tableGroups.grouped">
                <SidebarGroup
                    :collapsed="hiddenGroups.indexOf(String(groupName)) != -1"
                    :name="String(groupName)"
                    @toggled="toggleGroup(String(groupName))"
                />

                <template v-if="hiddenGroups.indexOf(String(groupName)) == -1">
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
import { defineComponent } from "vue"
import SidebarGroup from "./SidebarGroup.vue"
import TableNavItem from "./TableNavItem.vue"

export default defineComponent({
    components: {
        SidebarGroup,
        TableNavItem
    },
    data() {
        return {
            hiddenGroups: [] as string[]
        }
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
