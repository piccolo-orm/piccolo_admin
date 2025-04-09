<template>
    <BaseView>
        <template v-if="!loading">
            <div class="left_column">
                <div class="title_bar">
                    <div class="title">
                        <h1>{{ readable(tableName) }}</h1>
                        <Tooltip
                            :content="schema.extra.help_text"
                            v-if="schema.extra.help_text"
                        />
                    </div>
                    <div class="buttons">
                        <a
                            class="button"
                            href="#"
                            v-if="selectedRows.length > 0"
                            v-on:click.prevent="
                                showUpdateModal = !showUpdateModal
                            "
                        >
                            <font-awesome-icon icon="arrow-up" />
                            <span>
                                {{ $t("Update") }} {{ selectedRows.length }}
                                {{ $t("rows") }}</span
                            >
                        </a>
                        <BulkDeleteButton
                            :selected="selectedRows.length"
                            v-if="selectedRows.length > 0"
                            v-on:triggered="deleteRows"
                        />

                        <router-link
                            :to="{
                                name: 'addRow',
                                params: { tableName: tableName }
                            }"
                            class="button"
                            v-on:click.prevent="showAddRow = true"
                        >
                            <font-awesome-icon icon="plus" />
                            <span>{{ $t("Add Row") }}</span>
                        </router-link>

                        <a
                            class="button"
                            href="#"
                            v-on:click.prevent="showSortModal = !showSortModal"
                            data-uitest="sort_button"
                        >
                            <font-awesome-icon icon="sort" />
                            <span>{{ $t("Sort") }}</span>
                        </a>

                        <a
                            class="button"
                            href="#"
                            v-on:click.prevent="showFilter = !showFilter"
                            data-uitest="filter_button"
                        >
                            <font-awesome-icon icon="filter" />
                            <span>
                                {{
                                    showFilter
                                        ? $t("Hide Filters")
                                        : $t("Show Filters")
                                }}
                            </span>
                        </a>
                        <CSVButton />
                    </div>
                </div>
                <p id="selected_count" v-if="selectedRows.length > 0">
                    <b>{{ selectedRows.length }}</b>
                    {{ $t("selected result(s) on") }}
                    <b>{{ $t("page") }} {{ currentPageNumber }}</b>
                </p>

                <div class="table_wrapper">
                    <transition name="fade">
                        <p v-show="loadingStatus" id="loading_indicator">
                            {{ $t("Loading") }} ...
                        </p>
                    </transition>

                    <transition name="fade">
                        <div v-if="!loadingStatus && rows != undefined">
                            <p v-if="rows.length == 0">
                                {{ $t("No results found") }}
                            </p>
                            <template v-else>
                                <table>
                                    <thead>
                                        <tr>
                                            <th>
                                                <input
                                                    type="checkbox"
                                                    v-model="allSelected"
                                                    v-on:change="selectAllRows"
                                                />
                                            </th>
                                            <th
                                                v-bind:key="name"
                                                v-for="name in visibleColumnNames"
                                            >
                                                {{
                                                    schema.properties[name]
                                                        ? schema.properties[
                                                              name
                                                          ].title
                                                        : name
                                                }}

                                                <a
                                                    href="#"
                                                    @click.prevent="
                                                        showSortModal = true
                                                    "
                                                    v-if="orderByMapping[name]"
                                                >
                                                    <font-awesome-icon
                                                        icon="caret-up"
                                                        v-if="
                                                            orderByMapping[name]
                                                                .ascending
                                                        "
                                                    />
                                                    <font-awesome-icon
                                                        icon="caret-down"
                                                        v-else
                                                    />
                                                </a>
                                            </th>
                                            <th></th>
                                        </tr>
                                    </thead>

                                    <tbody>
                                        <tr
                                            v-bind:key="row[pkName]"
                                            v-for="row in rows"
                                        >
                                            <td>
                                                <input
                                                    :value="row[pkName]"
                                                    @click="selectRow"
                                                    type="checkbox"
                                                    v-model="selectedRows"
                                                />
                                            </td>
                                            <td
                                                v-bind:key="name"
                                                v-for="name in visibleColumnNames"
                                            >
                                                <span v-if="row[name] === null">
                                                    <code>NULL</code>
                                                </span>
                                                <span
                                                    class="link"
                                                    v-else-if="
                                                        name == linkColumnName
                                                    "
                                                >
                                                    <router-link
                                                        :to="{
                                                            name: 'editRow',
                                                            params: {
                                                                tableName:
                                                                    tableName,
                                                                rowID: row[
                                                                    pkName
                                                                ]
                                                            }
                                                        }"
                                                        >{{
                                                            row[name]
                                                        }}</router-link
                                                    >
                                                </span>
                                                <span
                                                    v-else-if="
                                                        choicesLookup[name]
                                                    "
                                                >
                                                    <template
                                                        v-if="isArray(name)"
                                                    >
                                                        {{
                                                            abbreviate(
                                                                row[name]
                                                                    .map(
                                                                        (
                                                                            i: any
                                                                        ) =>
                                                                            choicesLookup[
                                                                                name
                                                                            ]![
                                                                                i
                                                                            ] ??
                                                                            i
                                                                    )
                                                                    .join(", ")
                                                            )
                                                        }}
                                                    </template>
                                                    <template v-else>{{
                                                        choicesLookup[name]![
                                                            row[name]
                                                        ] ?? row[name]
                                                    }}</template>
                                                </span>
                                                <span
                                                    class="link"
                                                    v-else-if="
                                                        isForeignKey(name) &&
                                                        row[name] !== null
                                                    "
                                                >
                                                    <router-link
                                                        :to="{
                                                            name: 'editRow',
                                                            params: {
                                                                tableName:
                                                                    getTableName(
                                                                        name
                                                                    ),
                                                                rowID: row[name]
                                                            }
                                                        }"
                                                        >{{
                                                            row[
                                                                name +
                                                                    "_readable"
                                                            ]
                                                        }}</router-link
                                                    >
                                                </span>
                                                <span
                                                    class="boolean"
                                                    v-else-if="isBoolean(name)"
                                                >
                                                    <font-awesome-icon
                                                        class="correct"
                                                        icon="check"
                                                        v-if="
                                                            row[name] === true
                                                        "
                                                    />
                                                    <font-awesome-icon
                                                        class="incorrect"
                                                        icon="times"
                                                        v-else-if="
                                                            row[name] === false
                                                        "
                                                    />
                                                </span>
                                                <span
                                                    v-else-if="isInterval(name)"
                                                >
                                                    {{
                                                        humanReadable(row[name])
                                                    }}
                                                </span>
                                                <span v-else-if="isJSON(name)">
                                                    <pre>{{
                                                        abbreviate(
                                                            formatJSON(
                                                                row[name]
                                                            )
                                                        )
                                                    }}</pre>
                                                </span>
                                                <span
                                                    v-else-if="
                                                        isMediaColumn(name)
                                                    "
                                                >
                                                    <template
                                                        v-if="isArray(name)"
                                                    >
                                                        <a
                                                            style="
                                                                display: block;
                                                            "
                                                            href="#"
                                                            v-for="item in row[
                                                                name
                                                            ]"
                                                            :key="item"
                                                            @click.prevent="
                                                                showMedia(
                                                                    item,
                                                                    name
                                                                )
                                                            "
                                                            >{{
                                                                abbreviate(item)
                                                            }}
                                                        </a>
                                                    </template>
                                                    <template v-else>
                                                        <a
                                                            href="#"
                                                            @click.prevent="
                                                                showMedia(
                                                                    row[name],
                                                                    name
                                                                )
                                                            "
                                                            >{{
                                                                abbreviate(
                                                                    row[name]
                                                                )
                                                            }}
                                                        </a>
                                                    </template>
                                                </span>
                                                <span v-else>
                                                    {{ abbreviate(row[name]) }}
                                                </span>
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
                                                            visibleDropdown =
                                                                visibleDropdown
                                                                    ? undefined
                                                                    : row[
                                                                          pkName
                                                                      ]
                                                        "
                                                    >
                                                        <font-awesome-icon
                                                            icon="ellipsis-v"
                                                        />
                                                    </a>
                                                    <DropDownMenu
                                                        v-if="
                                                            visibleDropdown ==
                                                            row[pkName]
                                                        "
                                                    >
                                                        <li>
                                                            <router-link
                                                                :to="{
                                                                    name: 'editRow',
                                                                    params: {
                                                                        tableName:
                                                                            tableName,
                                                                        rowID: row[
                                                                            pkName
                                                                        ]
                                                                    }
                                                                }"
                                                                class="subtle"
                                                                title="Edit Row"
                                                            >
                                                                <font-awesome-icon
                                                                    icon="edit"
                                                                />{{
                                                                    $t("Edit")
                                                                }}
                                                            </router-link>
                                                        </li>
                                                        <li>
                                                            <DeleteButton
                                                                :includeTitle="
                                                                    true
                                                                "
                                                                class="subtle delete"
                                                                v-on:triggered="
                                                                    deleteRow(
                                                                        row[
                                                                            pkName
                                                                        ]
                                                                    )
                                                                "
                                                            />
                                                        </li>
                                                    </DropDownMenu>
                                                </span>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>

                                <p id="result_count">
                                    {{ $t("Showing") }} {{ rows.length }}
                                    {{ $t("of") }}
                                    {{ rowCount }}
                                    {{ $t("result(s)") }}
                                </p>

                                <div class="pagination_wrapper">
                                    <Pagination :tableName="tableName" />
                                    <ChangePageSize />
                                </div>
                            </template>
                        </div>
                    </transition>
                </div>
            </div>

            <div
                class="right_column"
                v-if="showFilter"
                data-uitest="right_sidebar"
            >
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

            <OrderByModal
                :schema="schema"
                :tableName="tableName"
                v-if="showSortModal"
                v-on:close="showSortModal = false"
            />

            <BulkUpdateModal
                :schema="schema"
                :tableName="tableName"
                :selectedRows="selectedRows"
                v-if="showUpdateModal"
                v-on:close="showUpdateModal = false"
            />

            <MediaViewer
                v-if="showMediaViewer"
                :mediaViewerConfig="mediaViewerConfig"
                @close="showMediaViewer = false"
            />
        </template>
    </BaseView>
</template>

<script lang="ts">
import axios from "axios"
import { defineComponent, type PropType } from "vue"

import AddRowModal from "../components/AddRowModal.vue"
import BaseView from "./BaseView.vue"
import BulkUpdateModal from "../components/BulkUpdateModal.vue"
import BulkDeleteButton from "../components/BulkDeleteButton.vue"
import CSVButton from "../components/CSVButton.vue"
import DeleteButton from "../components/DeleteButton.vue"
import DropDownMenu from "../components/DropDownMenu.vue"
import ChangePageSize from "../components/ChangePageSize.vue"
import MediaViewer from "../components/MediaViewer.vue"
import Pagination from "../components/Pagination.vue"
import RowFilter from "../components/RowFilter.vue"
import OrderByModal from "../components/OrderByModal.vue"
import Tooltip from "../components/Tooltip.vue"
import {
    type APIResponseMessage,
    type Choice,
    type Schema,
    type MediaViewerConfig,
    type OrderByConfig,
    type RowID,
    getType,
    getFormat
} from "@/interfaces"
import {
    deserialiseOrderByString,
    parseErrorResponse,
    readableInterval,
    readable
} from "@/utils"

export default defineComponent({
    props: {
        tableName: {
            type: String as PropType<string>,
            required: true
        }
    },
    data() {
        return {
            selectedRows: [] as RowID[],
            allSelected: false,
            showAddRow: false,
            showFilter: false,
            showSortModal: false,
            showUpdateModal: false,
            visibleDropdown: null,
            showMediaViewer: false,
            mediaViewerConfig: undefined as MediaViewerConfig | undefined,
            loading: true
        }
    },
    components: {
        AddRowModal,
        BaseView,
        BulkDeleteButton,
        BulkUpdateModal,
        ChangePageSize,
        CSVButton,
        DeleteButton,
        DropDownMenu,
        MediaViewer,
        Pagination,
        RowFilter,
        OrderByModal,
        Tooltip
    },
    setup() {
        return {
            readable
        }
    },
    computed: {
        visibleColumnNames() {
            return this.schema.extra.visible_column_names
        },
        rows() {
            return this.$store.state.rows
        },
        schema(): Schema {
            return this.$store.state.schema
        },
        orderBy(): OrderByConfig[] | null {
            return this.$store.state.orderBy
        },
        orderByMapping(): { [key: string]: OrderByConfig } {
            const orderBy: OrderByConfig[] | null = this.orderBy

            if (!orderBy) {
                return {}
            }

            return Object.fromEntries(orderBy.map((i) => [i.column, i]))
        },
        rowCount() {
            return this.$store.state.rowCount
        },
        currentPageNumber() {
            return this.$store.state.currentPageNumber
        },
        loadingStatus() {
            return this.$store.state.loadingStatus
        },
        pkName() {
            return this.schema.extra.primary_key_name || "id"
        },
        linkColumnName(): string {
            let schema: Schema = this.schema
            return schema.extra.link_column_name
        },
        // We create an object for quickly mapping a choice value to it's
        // display value. It maps column name -> choice value -> display value.
        // For example {'genre': {1: 'Sci-Fi'}}
        choicesLookup() {
            let schema = this.schema
            const output: {
                [key: string]: { [key: string | number]: string } | null
            } = {}

            for (const [columnName, config] of Object.entries(
                schema.properties
            )) {
                const choices = config.extra.choices

                const reducer = (
                    accumulator: { [key: string]: any },
                    choice: Choice
                ) => {
                    accumulator[choice.value] = choice.display_name
                    return accumulator
                }

                if (choices) {
                    output[columnName] = Object.values(choices).reduce(
                        reducer,
                        {}
                    )
                } else {
                    output[columnName] = null
                }
            }
            return output
        }
    },
    methods: {
        abbreviate(value: string | null) {
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
        humanReadable(value: string) {
            return readableInterval(value)
        },
        formatJSON(value: string) {
            return JSON.stringify(JSON.parse(value), null, 2)
        },
        isForeignKey(name: string): boolean {
            return this.schema.properties[name]?.extra.foreign_key !== undefined
        },
        isBoolean(name: string): boolean {
            return getType(this.schema.properties[name]) == "boolean"
        },
        isInterval(name: string): boolean {
            return getFormat(this.schema.properties[name]) == "duration"
        },
        isJSON(name: string): boolean {
            return this.schema.properties[name].extra?.widget == "json"
        },
        isArray(name: string): boolean {
            return getType(this.schema.properties[name]) == "array"
        },
        isMediaColumn(name: string): boolean {
            return this.schema.extra.media_columns.includes(name)
        },
        getTableName(name: string) {
            // Find the table name a foreign key refers to.
            return this.schema.properties[name]!.extra.foreign_key!.to
        },
        closeSideBar() {
            this.showFilter = false
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
                this.selectedRows = this.rows.map(
                    (row: any) => row[this.pkName]
                )
            } else {
                this.selectedRows = []
            }
        },
        showSuccess(contents: string) {
            var message: APIResponseMessage = {
                contents: contents,
                type: "success"
            }
            this.$store.commit("updateApiResponseMessage", message)
        },
        async showMedia(fileKey: string, columnName: string) {
            const tableName = this.$store.state.currentTableName
            this.mediaViewerConfig = {
                fileKey,
                columnName,
                tableName
            }
            this.showMediaViewer = true
        },
        async deleteRow(rowID: RowID) {
            if (confirm(`Are you sure you want to delete row ${rowID}?`)) {
                console.log("Deleting!")
                await this.$store.dispatch("deleteRow", {
                    tableName: this.tableName,
                    rowID
                })
                await this.fetchRows()
                this.showSuccess("Successfully deleted row")
            }
        },
        async deleteRows() {
            if (confirm(`Are you sure you want to delete the selected rows?`)) {
                console.log("Deleting rows!")

                for (let i = 0; i < this.selectedRows.length; i++) {
                    try {
                        await this.$store.dispatch("deleteRow", {
                            tableName: this.tableName,
                            rowID: this.selectedRows[i]
                        })
                    } catch (error) {
                        if (axios.isAxiosError(error) && error.response) {
                            const errors = parseErrorResponse(
                                error.response.data,
                                error.response.status
                            )
                            const errorString = errors.join(", ")

                            var message: APIResponseMessage = {
                                contents: `Unable to delete row ${this.selectedRows[i]} (${errorString})`,
                                type: "error"
                            }
                            this.$store.commit(
                                "updateApiResponseMessage",
                                message
                            )
                            await this.fetchRows()
                        }

                        return
                    }
                }
                await this.fetchRows()
                this.showSuccess("Successfully deleted rows")
            }
        },
        async fetchRows() {
            await this.$store.dispatch("fetchRows")
        },
        async fetchSchema() {
            await this.$store.dispatch("fetchSchema", this.tableName)

            const orderBy = this.$route.query.__order as string
            if (orderBy) {
                this.$store.commit(
                    "updateOrderBy",
                    deserialiseOrderByString(orderBy)
                )
            } else {
                this.$store.commit("updateOrderBy", this.schema.extra.order_by)
            }
        }
    },
    watch: {
        "$route.params.tableName": async function () {
            this.loading = true
            this.$store.commit("reset")
            this.$store.commit("updateCurrentTablename", this.tableName)
            await this.fetchSchema()
            await this.fetchRows()
            this.loading = false
        },
        "$route.query": async function () {
            this.$store.commit(
                "updateFilterParams",
                this.$router.currentRoute.value.query
            )
            await this.fetchRows()
        },
        rows() {
            this.resetRowCheckbox()
        }
    },
    async mounted() {
        this.loading = true
        this.$store.commit("updateCurrentTablename", this.tableName)

        this.$store.commit(
            "updateFilterParams",
            this.$router.currentRoute.value.query
        )

        await this.fetchSchema()
        await this.fetchRows()
        this.loading = false
    }
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

        div.title {
            flex-grow: 1;
            display: flex;
            align-items: center;

            h1 {
                display: inline-block;
                text-transform: capitalize;
                margin: 0 0.5rem 0 0;
            }
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

                &:hover {
                    color: white;
                }

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

        div.table_wrapper {
            position: relative;

            p#loading_indicator {
                position: absolute;
                top: 0;
                left: 0;
            }

            .fade-enter-active,
            .fade-leave-active {
                transition: opacity 0.8s;
            }

            .fade-enter-from,
            .fade-leave-to {
                opacity: 0;
                transition: opacity 0s;
            }

            table {
                border-collapse: collapse;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: -1px 0px 2px 1px rgba(0, 0, 0, 0.1);
                width: 100%;

                tr {
                    text-align: left;

                    span.boolean {
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
                    white-space: nowrap;

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
