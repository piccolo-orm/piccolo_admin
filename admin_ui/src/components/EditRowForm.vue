<template>
    <div v-if="schema">
        <div class="header">
            <h1>Edit {{ readable(tableName) }}</h1>

            <p>
                <a
                    class="subtle"
                    href="#"
                    v-on:click.prevent="showDropdown = !showDropdown"
                >
                    <font-awesome-icon icon="ellipsis-v" />
                    <DropDownMenu v-if="showDropdown">
                        <li>
                            <DeleteButton
                                :includeTitle="true"
                                class="subtle"
                                v-on:triggered="deleteRow"
                            />
                        </li>
                    </DropDownMenu>
                </a>
            </p>
        </div>

        <pre>{{ errors }}</pre>

        <form v-on:submit.prevent="submitForm($event)">
            <RowFormSelect
                :row="selectedRow"
                :schema="schema"
            />
            <button>Save</button>
        </form>

        <ReferencingTables
            :rowID="rowID"
            :tableName="tableName"
        />
    </div>
</template>


<script lang="ts">
import { defineComponent } from "vue"
import ReferencingTables from "./ReferencingTables.vue"
import DeleteButton from "./DeleteButton.vue"
import DropDownMenu from "./DropDownMenu.vue"
import RowFormSelect from "./RowFormSelect.vue"

import { APIResponseMessage, UpdateRow, DeleteRow } from "../interfaces"

export default defineComponent({
    props: ["tableName", "rowID"],
    components: {
        DeleteButton,
        DropDownMenu,
        RowFormSelect,
        ReferencingTables,
    },
    data() {
        return {
            errors: "",
            showDropdown: false,
        }
    },
    computed: {
        schema(): any {
            return this.$store.state.schema
        },
        selectedRow(): any {
            return this.$store.state.selectedRow
        },
    },
    methods: {
        readable(value: string) {
            return value.split("_").join(" ")
        },
        async submitForm(event: any) {
            console.log("Submitting...")
            const form = new FormData(event.target)

            const json = {} as any
            for (const i of form.entries()) {
                const key = i[0].split(" ").join("_")
                let value: any = i[1]

                if (value == "null") {
                    value = null
                } else if (this.schema.properties[key].type == "array") {
                    // @ts-ignore
                    value = JSON.parse(value)
                } else if (
                    this.schema?.properties[key].format == "date-time" &&
                    value == ""
                ) {
                    value = null
                } else if (
                    this.schema?.properties[key].extra.foreign_key == true &&
                    value == ""
                ) {
                    value = null
                }
                json[key] = value
            }

            let config: UpdateRow = {
                tableName: this.tableName,
                rowID: this.rowID,
                data: json,
            }
            try {
                await this.$store.dispatch("updateRow", config)
            } catch (error) {
                const data = error.response.data

                var message: APIResponseMessage = {
                    contents: "The form has errors.",
                    type: "error",
                }
                this.$store.commit("updateApiResponseMessage", message)

                if (typeof data != "string") {
                    this.errors = JSON.stringify(data, null, 2)
                } else {
                    this.errors = data
                }
                return
            }
            this.errors = ""

            if (opener) {
                opener.postMessage("edited row", document.location.origin)
            }
        },
        async deleteRow() {
            if (window.confirm("Are you sure you want to delete this row?")) {
                let config: DeleteRow = {
                    tableName: this.tableName,
                    rowID: this.rowID,
                }
                await this.$store.dispatch("deleteRow", config)
                alert("Successfully deleted row")
                this.$router.push({
                    name: "rowListing",
                    params: { tableName: this.tableName },
                })
            }
        },
        async fetchData() {
            this.$store.commit("updateCurrentTablename", this.tableName)
            await this.$store.dispatch("fetchSingleRow", {
                tableName: this.tableName,
                rowID: this.rowID,
            })
        },
    },
    watch: {
        "$route.params.tableName": async function () {
            await Promise.all([
                this.fetchData(),
                this.$store.dispatch("fetchSchema", this.tableName),
            ])
        },
        "$route.params.rowID": async function () {
            await this.fetchData()
        },
    },
    async mounted() {
        await Promise.all([
            this.fetchData(),
            this.$store.dispatch("fetchSchema", this.tableName),
        ])
    },
})
</script>


<style scoped lang="less">
@import "../vars.less";

div.header {
    align-items: center;
    display: flex;
    flex-direction: row;

    h1 {
        text-transform: capitalize;
        flex-grow: 1;
    }
    p {
        flex-grow: 0;
        position: relative;
        text-align: right;

        a {
            font-weight: bold;
            text-decoration: none;
        }
    }

    li {
        a {
            color: white;
        }
    }
}
</style>
