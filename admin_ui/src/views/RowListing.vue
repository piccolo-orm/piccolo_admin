<template>
    <BaseView>
        <template v-if="schema != undefined">
            <div class="left_column">
                <div class="title_bar">
                    <h1>{{ tableName }}</h1>
                    <ul>
                        <li>
                            <a
                                href="#"
                                v-on:click.prevent="showAddRow = true"
                            >
                                <font-awesome-icon icon="plus" />Add Row
                            </a>
                        </li>
                        <li>
                            <a
                                href="#"
                                v-on:click.prevent="showFilter = !showFilter"
                            >
                                <font-awesome-icon icon="filter" />{{ showFilter ? "Hide" : "Show" }} Filters
                            </a>
                        </li>
                    </ul>
                </div>

                <p v-if="rows.length == 0">No results found</p>
                <table v-else>
                    <tr>
                        <th
                            v-bind:key="name"
                            v-for="name in cellNames"
                        >{{ name }}</th>
                        <th>Actions</th>
                    </tr>

                    <tr
                        v-bind:key="row.id"
                        v-for="row in rows"
                    >
                        <td
                            v-bind:key="name"
                            v-for="(cell, name) in row"
                        >
                            <span
                                class="link"
                                v-if="name == 'id'"
                            >
                                <router-link
                                    :to="{name: 'editRow', params: {tableName: tableName, rowID: cell }}"
                                >{{ cell }}</router-link>
                            </span>
                            <span
                                class="link"
                                v-else-if="isForeignKey(name)"
                            >
                                <router-link
                                    :to="{name: 'editRow', params: {tableName: getTableName(name), rowID: cell }}"
                                >{{ cell }}</router-link>
                            </span>
                            <span v-else>{{ cell }}</span>
                        </td>

                        <td class="snug">
                            <ul>
                                <li>
                                    <router-link
                                        :to="{name: 'editRow', params: {tableName: tableName, rowID: row.id}}"
                                        title="Edit Row"
                                    >
                                        <font-awesome-icon icon="edit" />
                                    </router-link>
                                </li>
                                <li>
                                    <a
                                        class="delete"
                                        href="#"
                                        title="Delete Row"
                                        v-on:click.prevent="deleteRow(row.id)"
                                    >
                                        <font-awesome-icon icon="trash-alt" />
                                    </a>
                                </li>
                            </ul>
                        </td>
                    </tr>
                </table>
            </div>

            <div class="right_column" v-if="showFilter">
                <RowFilter />
            </div>

            <AddRow
                v-bind:schema="schema"
                v-bind:tableName="tableName"
                v-if="showAddRow"
                v-on:addedRow="fetchRows"
                v-on:close="showAddRow = false"
            />
        </template>
    </BaseView>
</template>


<script lang="ts">
import Vue from "vue"
import axios from "axios"
import AddRow from "../components/AddRow.vue"
import BaseView from "./BaseView.vue"
import RowFilter from "../components/RowFilter.vue"
import TableNav from "../components/TableNav.vue"

export default Vue.extend({
    props: ["tableName"],
    data() {
        return {
            showAddRow: false,
            showFilter: false
        }
    },
    components: {
        AddRow,
        BaseView,
        RowFilter,
        TableNav
    },
    computed: {
        cellNames() {
            const keys = []
            for (const key in this.rows[0]) {
                keys.push(key)
            }
            return keys
        },
        rows() {
            return this.$store.state.rows
        },
        schema() {
            return this.$store.state.schema
        }
    },
    methods: {
        isForeignKey(name: string) {
            let property = this.schema.properties[name]
            return property != undefined ? property.foreign_key : false
        },
        getTableName(name: string) {
            // Find the table name a foreign key refers to:
            return this.schema.properties[name].to
        },
        async deleteRow(rowID) {
            if (confirm(`Are you sure you want to delete row ${rowID}?`)) {
                console.log("Deleting!")
                await this.$store.dispatch("deleteRow", {
                    tableName: this.tableName,
                    rowID
                })
                await this.fetchRows()
            }
        },
        async fetchRows() {
            await this.$store.dispatch("fetchRows", {
                tableName: this.tableName,
                params: {}
            })
        },
        async fetchSchema() {
            await this.$store.dispatch("fetchSchema", this.tableName)
        }
    },
    watch: {
        "$route.params.tableName": async function(id) {
            this.$store.commit("updateCurrentTablename", this.tableName)
            this.$store.commit("updateRows", [])
            await Promise.all([this.fetchRows(), this.fetchSchema()])
        }
    },
    async mounted() {
        this.$store.commit("updateCurrentTablename", this.tableName)
        await Promise.all([this.fetchRows(), this.fetchSchema()])
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

        h1 {
            text-transform: capitalize;
            flex-grow: 1;
        }

        p {
            flex-grow: 0;
        }

        ul {
            li {
                display: inline-block;
                padding-left: 1rem;

                a {
                    text-decoration: none;
                }
            }
        }
    }

    div.left_column,
    div.right_column {
        overflow: scroll;
        padding: 0.5rem;
    }

    div.left_column {
        width: 80%;

        table {
            border-collapse: collapse;
            width: 100%;

            tr {
                border-bottom: 1px solid @border_color;
                text-align: left;
            }
            th {
                font-size: 0.8em;
                text-transform: uppercase;

                &:last-child {
                    text-align: right;
                }
            }
            td,
            th {
                padding: 0.5rem;
            }
            td {
                &.last-child {
                    text-align: right;
                    width: auto;
                }

                span.link {
                    a {
                        color: @light_blue;
                    }
                }

                a {
                    // color: rgba(255,255,255,0.6);
                    text-decoration: none;

                    &.delete:hover {
                        color: #ff6161;
                    }

                    &:hover {
                        color: @light_blue;
                    }
                }

                ul {
                    padding: 0;
                    text-align: right;

                    li {
                        display: inline-block;
                        margin-left: 0.5rem;
                    }
                }
            }
        }
    }

    div.right_column {
        border-left: 1px solid @border_color;
        box-sizing: border-box;
        padding: 1rem;
        width: 20rem;
    }
}
</style>
