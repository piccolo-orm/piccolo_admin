<template>
    <BaseView>
        <template v-if="schema != undefined">
            <div class="left_column">
                <TitleBar
                    :title="tableName | readable"
                    :titleTooltip="schema.help_text"
                >
                    <template v-slot:buttons>
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
                    </template>
                </TitleBar>

                <p id="selected_count" v-if="selectedRows.length > 0">
                    <b>{{ selectedRows.length }}</b>
                    selected result(s) on
                    <b>page {{ currentPageNumber }}</b>
                </p>

                <p v-if="rows.length == 0">No results found</p>
                <Table v-else>
                    <template v-slot:thead>
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
                    </template>

                    <template v-slot:tbody>
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
                                        isForeignKey(name) &
                                        (row[name] !== null)
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
                                        >{{
                                            row[name + "_readable"]
                                        }}</router-link
                                    >
                                </span>

                                <BooleanIcon
                                    v-else-if="isBoolean(name)"
                                    v-bind:boolean="row[name] === true"
                                />
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
                                    <DropDownMenu
                                        v-if="visibleDropdown == row.id"
                                    >
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
                                                v-on:triggered="
                                                    deleteRow(row.id)
                                                "
                                            />
                                        </li>
                                    </DropDownMenu>
                                </span>
                            </td>
                        </tr>
                    </template>
                </Table>

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
import BooleanIcon from "../components/BooleanIcon.vue"
import BulkDeleteButton from "../components/BulkDeleteButton.vue"
import CSVButton from "../components/CSVButton.vue"
import DeleteButton from "../components/DeleteButton.vue"
import DropDownMenu from "../components/DropDownMenu.vue"
import ChangePageSize from "../components/ChangePageSize.vue"
import Pagination from "../components/Pagination.vue"
import RowFilter from "../components/RowFilter.vue"
import RowSortModal from "../components/RowSortModal.vue"
import Table from "../components/Table.vue"
import TableNav from "../components/TableNav.vue"
import TitleBar from "../components/TitleBar.vue"
import Tooltip from "../components/Tooltip.vue"

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
        BooleanIcon,
        BulkDeleteButton,
        CSVButton,
        DeleteButton,
        DropDownMenu,
        Pagination,
        ChangePageSize,
        RowFilter,
        RowSortModal,
        Table,
        TableNav,
        TitleBar,
        Tooltip,
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
    div.left_column,
    div.right_column {
        overflow: auto;
        padding: 0.5rem;
    }

    div.left_column {
        width: 100%;
        padding: 0.5rem 0.8rem;

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
