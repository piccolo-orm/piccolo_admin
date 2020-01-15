<template>
    <div v-if="references.length > 0">
        <p class="referencing_title">
            <a
                href="#"
                v-on:click.prevent="showReferencing = !showReferencing"
            >
                <span v-if="showReferencing">
                    <font-awesome-icon icon="angle-down" />Hide
                </span>
                <span v-else>
                    <font-awesome-icon icon="angle-right" />Show
                </span> Referencing Tables
            </a>
        </p>
        <ul
            class="related_tables"
            v-if="showReferencing"
        >
            <li
                v-bind:key="reference.tableName + reference.columnName"
                v-for="reference in references"
            >
                <a
                    href="#"
                    v-on:click.prevent="clickedReference(reference)"
                >
                    <span class="table">{{ reference.tableName }}</span>
                    ({{ reference.columnName }} column)
                    <font-awesome-icon icon="external-link-alt" />
                </a>
            </li>
        </ul>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import { Location } from "vue-router"
import { TableReferencesAPIResponse, TableReference } from "../interfaces"

export default Vue.extend({
    props: ["tableName", "rowID"],
    data: function() {
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
            this.references = (response.data as TableReferencesAPIResponse).references
        },
        clickedReference(reference: TableReference) {
            let columnName = reference.columnName
            let query = {}
            query[columnName] = this.rowID

            let location: Location = {
                name: "rowListing",
                params: { tableName: reference.tableName },
                query
            }
            let vueUrl = this.$router.resolve(location).href
            window.open(
                `${document.location.origin}${document.location.pathname}${vueUrl}`,
                "_blank"
            )
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
    margin-top: 1rem;
    padding: 0.5rem 0;
}

ul.related_tables {
    li {
        span.table {
            font-weight: bold;
            text-transform: capitalize;
        }
    }
}
</style>
