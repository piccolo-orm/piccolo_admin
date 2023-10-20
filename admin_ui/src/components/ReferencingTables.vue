<template>
    <div v-if="references.length > 0">
        <p class="referencing_title">
            <a href="#" v-on:click.prevent="showReferencing = !showReferencing">
                <span v-if="showReferencing">
                    <font-awesome-icon icon="angle-down" />{{
                        $t("Hide referencing tables")
                    }}
                </span>
                <span v-else>
                    <font-awesome-icon icon="angle-right" />{{
                        $t("Show referencing tables")
                    }}
                </span>
            </a>
        </p>
        <ul class="related_tables" v-if="showReferencing">
            <li
                v-bind:key="reference.tableName + reference.columnName"
                v-for="reference in references"
            >
                <router-link
                    :to="{
                        name: 'rowListing',
                        params: { tableName: reference.tableName },
                        query: getQueryParams(reference)
                    }"
                >
                    <font-awesome-icon icon="level-up-alt" class="rotated90" />
                    <span class="table bold">{{ reference.tableName }}</span>
                    {{ $t("with a matching") }}
                    <span class="bold">{{
                        reference.columnName
                    }}</span></router-link
                >
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"
import type { TableReferencesAPIResponse, TableReference } from "../interfaces"

export default defineComponent({
    props: {
        tableName: {
            type: String as PropType<string>
        },
        rowID: {
            type: undefined as unknown as PropType<number | string>
        }
    },
    data: function () {
        return {
            references: [] as TableReference[],
            showReferencing: false
        }
    },
    methods: {
        async fetchTableReferences() {
            const response = await this.$store.dispatch(
                "fetchTableReferences",
                this.tableName
            )
            this.references = (
                response.data as TableReferencesAPIResponse
            ).references
        },
        getQueryParams(reference: TableReference) {
            const query: { [key: string]: any } = {}
            query[reference.columnName] = this.rowID
            return query
        }
    },
    async mounted() {
        await this.fetchTableReferences()
    }
})
</script>

<style scoped lang="less">
@import "../vars.less";

a {
    text-decoration: none;
}

p.referencing_title {
    color: @border_color;
    font-size: 0.8rem;
    margin-bottom: 0rem;
    margin-top: 1rem;
    padding: 0.5rem 0;
}

ul.related_tables {
    padding-left: 1rem;
    padding-top: 0;
    margin-top: 0;

    li {
        list-style: none;

        span.table {
            text-transform: capitalize;
        }
        span.bold {
            font-weight: bold;
        }

        svg {
            padding-left: 0.5rem;
        }
    }
}
</style>
