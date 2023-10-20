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
                        @click.prevent="toggleGroup(String(groupName))"
                        title="Click to toggle children."
                    >
                        <font-awesome-icon icon="layer-group" />
                        <span class="name">{{ groupName }}</span>
                        <span
                            class="ellipsis"
                            v-if="hiddenGroups.indexOf(String(groupName)) != -1"
                            >...</span
                        >
                    </a>
                </li>

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
import TableNavItem from "./TableNavItem.vue"

export default defineComponent({
    components: {
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

<style scoped lang="less">
li.group {
    font-size: 0.7em;

    a {
        text-transform: uppercase;

        span {
            &.name {
                padding-left: 0;
            }

            &.ellipsis {
                flex-grow: 1;
                text-align: right;
            }
        }
    }
}
</style>
