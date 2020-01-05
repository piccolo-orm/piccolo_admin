<template>
    <div>
        <NavBar />
        <div
            class="edit_wrapper"
            v-if="schema"
        >
            <p>
                <a
                    href="#"
                    v-on:click.prevent="$router.go(-1)"
                >
                    <font-awesome-icon icon="angle-left" />Back
                </a>
            </p>

            <h1>Edit</h1>

            <pre>{{ errors }}</pre>

            <form v-on:submit.prevent="submitForm($event)">
                <RowForm
                    v-bind:row="selectedRow"
                    v-bind:schema="schema"
                />
                <button>Save</button>
            </form>

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
                            ({{ reference.columnName }})
                            <font-awesome-icon icon="external-link-alt" />
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import { Location } from "vue-router"
import NavBar from "../components/NavBar.vue"
import RowForm from "../components/RowForm.vue"
import {
    UpdateRow,
    TableReferencesAPIResponse,
    TableReference
} from "../interfaces"

export default Vue.extend({
    props: ["tableName", "rowID"],
    components: {
        RowForm,
        NavBar
    },
    data: function() {
        return {
            errors: "",
            references: [] as TableReference[],
            showReferencing: false
        }
    },
    computed: {
        schema() {
            return this.$store.state.schema
        },
        selectedRow() {
            return this.$store.state.selectedRow
        }
    },
    methods: {
        async submitForm(event) {
            console.log("Submitting...")

            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                json[i[0].split(" ").join("_")] = i[1]
            }

            let config: UpdateRow = {
                tableName: this.tableName,
                rowID: this.rowID,
                data: json
            }
            try {
                await this.$store.dispatch("updateRow", config)
            } catch (error) {
                this.errors = error.response.data
                return
            }
            this.errors = ""
        },
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
        this.$store.commit("updateCurrentTablename", this.tableName)
        await Promise.all([
            this.$store.dispatch("fetchSingleRow", {
                tableName: this.tableName,
                rowID: this.rowID
            }),
            this.$store.dispatch("fetchSchema", this.tableName),
            this.fetchTableReferences()
        ])
    }
})
</script>


<style scoped lang="less">
@import "../vars.less";

div.edit_wrapper {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;

    a {
        text-decoration: none;
    }

    h1 {
        margin: 0;
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
                text-transform: capitalize;
            }
        }
    }
}
</style>
