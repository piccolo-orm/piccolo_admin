<template>
    <BaseView>
        <template v-if="schema != undefined">
            <div class="left_column">
                <div class="title_bar">
                    <h1>{{ tableName | readable }}</h1>
                    <div class="buttons">
                        <BulkDeleteButton
                            :selected="selectedRows.length"
                            v-if="selectedRows.length > 0"
                            v-on:triggered="deleteRows"
                        />

                        <router-link
                            :to="{
                                name: 'addRow',
                                params: { tableName: tableName },
                            }"
                            class="button"
                            v-on:click.prevent="showAddRow = true"
                        >
                            <font-awesome-icon icon="plus" />
                            <span>Add Row</span>
                        </router-link>

                        <a
                            class="button"
                            href="#"
                            v-on:click.prevent="showSort = !showSort"
                        >
                            <font-awesome-icon icon="sort" />
                            <span>Sort</span>
                        </a>

                        <a
                            class="button"
                            href="#"
                            v-on:click.prevent="showFilter = !showFilter"
                        >
                            <font-awesome-icon icon="filter" />
                            <span
                                >{{
                                    showFilter ? "Hide" : "Show"
                                }}
                                Filters</span
                            >
                        </a>
                        <CSVButton :tableName="tableName" />
                    </div>
                </div>
                <p id="selected_count" v-if="selectedRows.length > 0">
                    <b>{{ selectedRows.length }}</b>
                    selected result(s) on
                    <b>page {{ currentPageNumber }}</b>
                </p>

                <p v-if="rows.length == 0">No results found</p>
                <table v-else>
                    <tr>
                        <th>
                            <input
                                type="checkbox"
                                v-model="allSelected"
                                v-on:change="selectAllRows"
                            />
                        </th>
                        <th v-bind:key="name" v-for="name in cellNames">
                            {{
                                schema.properties[name]
                                    ? schema.properties[name].title
                                    : name
                            }}
                        </th>
                        <th></th>
                    </tr>

                    <tr v-bind:key="row.id" v-for="row in rows">
                        <td>
                            <input
                                :value="row.id"
                                @click="selectRow"
                                type="checkbox"
                                v-model="selectedRows"
                            />
                        </td>
                        <td v-bind:key="name" v-for="name in cellNames">
                            <span class="link" v-if="name == 'id'">
                                <router-link
                                    :to="{
                                        name: 'editRow',
                                        params: {
                                            tableName: tableName,
                                            rowID: row[name],
                                        },
                                    }"
                                    >{{ row[name] }}</router-link
                                >
                            </span>
                            <span
                                class="link"
                                v-else-if="
                                    isForeignKey(name) & (row[name] !== null)
                                "
                            >
                                <router-link
                                    :to="{
                                        name: 'editRow',
                                        params: {
                                            tableName: getTableName(name),
                                            rowID: row[name],
                                        },
                                    }"
                                    >{{ row[name + "_readable"] }}</router-link
                                >
                            </span>
                            <span class="boolean" v-else-if="isBoolean(name)">
                                <font-awesome-icon
                                    class="correct"
                                    icon="check"
                                    v-if="row[name] === true"
                                />
                                <font-awesome-icon
                                    class="incorrect"
                                    icon="times"
                                    v-else
                                />
                            </span>
                            <span v-else-if="isInterval(name)">{{
                                row[name] | humanReadable
                            }}</span>
                            <span v-else>{{ row[name] | abbreviate }}</span>
                        </td>

                        <td>
                            <span
                                style="
                                    position: relative;
                                    display: block;
                                    text-align: right;
                                "
                            >
                                <a
                                    class="subtle"
                                    href="#"
                                    v-on:click.prevent="
                                        visibleDropdown = visibleDropdown
                                            ? undefined
                                            : row.id
                                    "
                                >
                                    <font-awesome-icon icon="ellipsis-v" />
                                </a>
                                <DropDownMenu v-if="visibleDropdown == row.id">
                                    <li>
                                        <router-link
                                            :to="{
                                                name: 'editRow',
                                                params: {
                                                    tableName: tableName,
                                                    rowID: row.id,
                                                },
                                            }"
                                            class="subtle"
                                            title="Edit Row"
                                        >
                                            <font-awesome-icon
                                                icon="edit"
                                            />Edit
                                        </router-link>
                                    </li>
                                    <li>
                                        <DeleteButton
                                            :includeTitle="true"
                                            class="subtle delete"
                                            v-on:triggered="deleteRow(row.id)"
                                        />
                                    </li>
                                </DropDownMenu>
                            </span>
                        </td>
                    </tr>
                </table>
                <p id="result_count">
                    Showing {{ rows.length }} of {{ rowCount }} result(s)
                </p>

                <div class="pagination_wrapper">
                    <Pagination :tableName="tableName" />
                    <ChangePageSize />
                </div>
            </div>

            <div class="right_column" v-if="showFilter">
                <RowFilter
                    :showFilterSidebar="showFilter"
                    @closeSideBar="closeSideBar"
                />
            </div>

            <AddRowModal
                :schema="schema"
                :tableName="tableName"
                v-if="showAddRow"
                v-on:addedRow="fetchRows"
                v-on:close="showAddRow = false"
            />

            <RowSortModal
                :schema="schema"
                :tableName="tableName"
                v-if="showSort"
                v-on:close="showSort = false"
            />
        </template>
    </BaseView>
</template>


<script lang="ts">
import Vue from "vue"
import { readableFormat } from "../utils"

import AddRowModal from "../components/AddRowModal.vue"
import BaseView from "./BaseView.vue"
import BulkDeleteButton from "../components/BulkDeleteButton.vue"
import CSVButton from "../components/CSVButton.vue"
import DeleteButton from "../components/DeleteButton.vue"
import DropDownMenu from "../components/DropDownMenu.vue"
import ChangePageSize from "../components/ChangePageSize.vue"
import Pagination from "../components/Pagination.vue"
import RowFilter from "../components/RowFilter.vue"
import RowSortModal from "../components/RowSortModal.vue"
import TableNav from "../components/TableNav.vue"

export default Vue.extend({
    props: ["tableName"],
    data() {
        return {
            selectedRows: [],
            allSelected: false,
            showAddRow: false,
            showFilter: false,
            showSort: false,
            visibleDropdown: null,
        }
    },
    components: {
        AddRowModal,
        BaseView,
        BulkDeleteButton,
        CSVButton,
        DeleteButton,
        DropDownMenu,
        Pagination,
        ChangePageSize,
        RowFilter,
        RowSortModal,
        TableNav,
    },
    computed: {
        cellNames() {
            const keys = []
            for (const key in this.rows[0]) {
                if (!key.endsWith("_readable")) {
                    keys.push(key)
                }
            }
            return keys
        },
        rows() {
            return this.$store.state.rows
        },
        schema() {
            return this.$store.state.schema
        },
        rowCount() {
            return this.$store.state.rowCount
        },
        currentPageNumber() {
            return this.$store.state.currentPageNumber
        },
    },
    filters: {
        abbreviate(value) {
            // We need to handle null values, and make sure text strings aren't
            // too long.
            if (value === null) {
                return null
            }
            let string = String(value)
            if (string.length > 100) {
                return string.substring(0, 80) + "..."
            }
            return string
        },
        humanReadable(value) {
            return readableFormat(value)
        },
    },
    methods: {
        isForeignKey(name: string) {
            let property = this.schema.properties[name]
            return property != undefined ? property.extra.foreign_key : false
        },
        isBoolean(name: string) {
            return this.schema.properties[name]["type"] == "boolean"
        },
        isInterval(name: string) {
            return this.schema.properties[name]["format"] == "time-delta"
        },
        getTableName(name: string) {
            // Find the table name a foreign key refers to:
            return this.schema.properties[name].extra.to
        },
        closeSideBar(value) {
            this.showFilter = value
        },
        resetRowCheckbox() {
            this.allSelected = false
            this.selectedRows = []
        },
        selectRow() {
            this.allSelected = false
        },
        selectAllRows() {
            // Select all checkboxes and add row ids to selected array:
            if (this.allSelected) {
                this.selectedRows = this.rows.map((row) => row.id)
            } else {
                this.selectedRows = []
            }
        },
        async deleteRow(rowID) {
            if (confirm(`Are you sure you want to delete row ${rowID}?`)) {
                console.log("Deleting!")
                await this.$store.dispatch("deleteRow", {
                    tableName: this.tableName,
                    rowID,
                })
                await this.fetchRows()
            }
        },
        async deleteRows() {
            if (confirm(`Are you sure you want to delete the selected rows?`)) {
                console.log("Deleting rows!")
                for (let i = 0; i < this.selectedRows.length; i++) {
                    await this.$store.dispatch("deleteRow", {
                        tableName: this.tableName,
                        rowID: this.selectedRows[i],
                    })
                }
                await this.fetchRows()
            }
        },
        async fetchRows() {
            await this.$store.dispatch("fetchRows")
        },
        async fetchSchema() {
            await this.$store.dispatch("fetchSchema", this.tableName)
        },
    },
    watch: {
        "$route.params.tableName": async function () {
            this.$store.commit("reset")
            this.$store.commit("updateCurrentTablename", this.tableName)
            await Promise.all([this.fetchRows(), this.fetchSchema()])
        },
        "$route.query": async function () {
            this.$store.commit(
                "updateFilterParams",
                this.$router.currentRoute.query
            )
            await this.fetchRows()
        },
        rows() {
            this.resetRowCheckbox()
        },
    },
    async mounted() {
        this.$store.commit("updateCurrentTablename", this.tableName)

        this.$store.commit(
            "updateFilterParams",
            this.$router.currentRoute.query
        )

        await Promise.all([this.fetchRows(), this.fetchSchema()])
    },
})
</script>


<style lang="less">
@import "../vars.less";

div.wrapper {
    div.title_bar {
        display: flex;
        flex-direction: row;
        align-items: center;
        padding: 0.5rem 0;

        @media (max-width: @mobile_width) {
            align-items: initial;
            flex-direction: column;
        }

        h1 {
            text-transform: capitalize;
            margin: 0 0.5rem 0 0;
            flex-grow: 1;
        }

        p {
            flex-grow: 0;
        }

        div.buttons {
            box-sizing: border-box;
            cursor: pointer;
            display: flex;
            flex-direction: row;

            @media (max-width: @mobile_width) {
                width: 100%;
            }

            a.button {
                display: block;
                flex-grow: 0;
                font-weight: bold;
                text-decoration: none;
                margin-left: 0.25rem;
                box-sizing: border-box;
                padding: 0.2rem 0.5rem;
                text-align: center;

                @media (max-width: @mobile_width) {
                    flex-grow: 1;

                    svg {
                        padding: 0 !important;
                    }
                }

                span {
                    @media (max-width: @mobile_width) {
                        display: block;
                    }
                }

                &:first-child {
                    margin-left: 0;
                }
            }
        }
    }

    div.left_column,
    div.right_column {
        overflow: auto;
        padding: 0.5rem;
    }

    div.left_column {
        width: 100%;
        padding: 0.5rem 0.8rem;

        table {
            border-collapse: collapse;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: -1px 0px 2px 1px rgba(0, 0, 0, 0.1);
            width: 100%;

            tr {
                text-align: left;

                span.boolean {
                    padding-left: 0.5rem;

                    svg.correct {
                        color: @green;
                    }
                    svg.incorrect {
                        color: @red;
                    }
                }
            }
            td {
                font-size: 0.9em;
            }
            th {
                font-size: 0.7em;
                text-transform: uppercase;

                &:last-child {
                    text-align: right;
                }
            }
            td,
            th {
                padding: 0.7rem;
            }
            td {
                &.last-child {
                    text-align: right;
                    width: auto;
                }

                a {
                    text-decoration: none;

                    &.delete:hover {
                        color: @red;
                    }
                }

                ul {
                    padding: 0;
                    text-align: right;
                    min-width: 4rem;

                    li {
                        display: inline-block;
                        margin-left: 0.5rem;
                    }
                }
            }
        }

        p#result_count,
        p#selected_count {
            font-size: 0.6em;
            text-transform: uppercase;
        }

        div.pagination_wrapper {
            display: flex;
            flex-direction: row;

            div {
                flex-grow: 1;

                &:last-child {
                    flex-grow: 0;
                }
            }
        }
    }

    div.right_column {
        border-left: 1px solid @border_color;
        box-sizing: border-box;
        padding: 0.5rem 0.8rem;
        width: 30rem;

        h1 {
            margin-top: 0.5rem;
        }

        @media (max-width: @mobile_width) {
            width: 110rem;
        }
    }
}
</style>
