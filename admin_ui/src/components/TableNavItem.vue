<template>
    <li>
        <router-link
            :to="{
                name: 'rowListing',
                params: { tableName: tableName }
            }"
            class="subtle"
            v-bind:class="{ active: isActive(tableName) }"
        >
            <font-awesome-icon icon="level-up-alt" class="rotated90" />
            <span>{{ readableTableName }}</span>
        </router-link>
    </li>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

export default defineComponent({
    props: {
        tableName: {
            type: String as PropType<string>,
            required: true
        }
    },
    computed: {
        currentTableName(): string {
            return this.$store.state.currentTableName
        },
        readableTableName(): string {
            return this.tableName.split("_").join(" ")
        }
    },
    methods: {
        isActive(tableName: string): boolean {
            return this.currentTableName === tableName
        }
    }
})
</script>
