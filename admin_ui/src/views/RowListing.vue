<template>
<div>
    <NavBar />
    <div class="wrapper">
        <div class="sidebar">
            <p><router-link to="/"><font-awesome-icon icon="home" /> Home</router-link></p>
            <p><font-awesome-icon icon="table" /> Tables</p>
            <TableNav />
        </div>

        <div class="left_column">
            <div class="title_bar">
                <h1>{{ tableName }}</h1>
                <ul>
                    <li>
                        <a href="#" v-on:click.prevent="showFilter = true"><font-awesome-icon icon="filter" /> Filter</a>
                    </li>
                    <li>
                        <a href="#"><font-awesome-icon icon="plus" /> Add Row</a>
                    </li>
                </ul>
            </div>

            <RowFilter
                v-if="showFilter"
                v-on:close="showFilter = false" />

            <p v-if="rows.length == 0">No results found</p>
            <table v-else>
                <tr>
                    <th v-for="name in cellNames" v-bind:key="name">{{ name }}</th>
                    <th>Actions</th>
                </tr>

                <tr v-for="row in rows" v-bind:key="row.id">
                    <td v-for="(cell, name) in row" v-bind:key="cell">
                        <span v-if="isForeignKey(name)">
                            <router-link :to="{name: 'editRow', params: {tableName: getTableName(name), rowID: row.id }}">{{ cell }}</router-link>
                        </span>
                        <span v-else>{{ cell }}</span>
                    </td>

                    <td class="snug">
                        <ul>
                            <li>
                                <router-link :to="{name: 'editRow', params: {tableName: tableName, rowID: row.id}}" title="Edit Row">
                                    <font-awesome-icon icon="edit" />
                                </router-link>
                            </li>
                            <li>
                                <a href="#" class="delete" v-on:click.prevent="deleteRow(row.id)" title="Delete Row">
                                    <font-awesome-icon icon="trash-alt" />
                                </a>
                            </li>
                        </ul>
                    </td>
                </tr>
            </table>
        </div>

        <div class="right_column">
            <h2>Add</h2>
            <form v-on:submit.prevent="submitForm($event)">
                <div v-for="property in schema.properties" v-bind:key="property.title">
                    <label>{{ property.title }}</label>

                    <input v-if="property.type == 'integer'" type="number" v-bind:name="property.title.toLowerCase()" />

                    <input v-if="property.type == 'string'" type="text" v-bind:name="property.title.toLowerCase()" />

                    <input v-if="property.type == 'boolean'" type="checkbox" v-bind:name="property.title.toLowerCase()" />
                </div>
                <button>Create</button>
            </form>
        </div>
    </div>
</div>
</template>


<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import RowFilter from '../components/RowFilter.vue'
import NavBar from '../components/NavBar.vue'
import TableNav from '../components/TableNav.vue'

export default Vue.extend({
    props: [
        'tableName'
    ],
    data() {
        return {
            showFilter: false
        }
    },
    components: {
        RowFilter,
        NavBar,
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
            return this.$store.state.rows;
        },
        schema() {
            return this.$store.state.schema;
        },
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
        async submitForm(event) {
            console.log('I was pressed')
            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                json[i[0]] = i[1]
            }
            const response = await this.$store.dispatch(
                'createRow',
                {
                    tableName: this.tableName,
                    data: json
                }
            )
            await this.fetchRows()
        },
        async deleteRow(rowID) {
            if (confirm(`Are you sure you want to delete row ${rowID}?`)) {
                console.log('Deleting!')
                await this.$store.dispatch(
                    'deleteRow',
                    {
                        tableName: this.tableName,
                        rowID
                    }
                )
                await this.fetchRows()
            }
        },
        async fetchRows() {
            await this.$store.dispatch(
                'fetchRows',
                {
                    tableName: this.tableName,
                    params: {}
                }
            )
        },
        async fetchSchema() {
            await this.$store.dispatch(
                'fetchSchema',
                this.tableName
            )
        }
    },
    watch: {
        '$route.params.tableName': async function(id) {
            this.$store.commit('updateCurrentTablename', this.tableName)
            this.$store.commit('updateRows', [])
            await Promise.all([
                this.fetchRows(),
                this.fetchSchema()
            ])
        }
    },
    async mounted() {
        this.$store.commit('updateCurrentTablename', this.tableName)
        await Promise.all([
            this.fetchRows(),
            this.fetchSchema()
        ])
    }
})
</script>


<style lang="less">
@border_color: rgba(255,255,255,0.2);
@light_blue: #009dff;

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
div.wrapper {
    border-top: 1px solid @border_color;
    display: flex;
    height: 100%;

    div.sidebar {
        border-right: 1px solid @border_color;
        width: 15rem;

        p {
            padding: 0.5rem;
            margin: 0;

            a {
                text-decoration: none;
            }
        }

        ul {
            margin: 0;

            li {
                a {
                    background-color: rgba(0,0,0,0.2);
                    display: block;
                    padding: 0.5rem;
                    text-decoration: none;

                    &:hover {
                        background-color: rgba(0,0,0,0.4);
                    }

                    &.active {
                        border-right: 3px solid @light_blue;
                    }
                }
            }
        }
    }

    div.left_column, div.right_column {
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
            td, th {
                padding: 0.5rem;
            }
            td {
                &.last-child {
                    text-align: right;
                    width: auto;
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
