<template>
    <div v-if="schema">
        <div class="header">
            <h1>{{ $t("Edit") }} {{ readable(tableName) }}</h1>

            <p>
                <a
                    class="subtle"
                    href="#"
                    data-uitest="drop_down_button"
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

        <FormErrors v-if="errors.length > 0" v-bind:errors="errors" />

        <form v-on:submit.prevent="submitForm($event)">
            <RowForm
                v-if="schema && selectedRow"
                :row="selectedRow"
                :schema="schema"
            />
            <button :disabled="!saveButtonEnabled" data-uitest="save_button">
                {{ $t("Save") }}
            </button>
        </form>

        <ReferencingTables :rowID="rowID" :tableName="tableName" />
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

import ReferencingTables from "./ReferencingTables.vue"
import DeleteButton from "./DeleteButton.vue"
import DropDownMenu from "./DropDownMenu.vue"
import RowForm from "./RowForm.vue"
import FormErrors from "./FormErrors.vue"
import { convertFormValue, readable } from "@/utils"

import type {
    APIResponseMessage,
    UpdateRow,
    DeleteRow,
    RowID
} from "../interfaces"
import { parseErrorResponse } from "../utils"
import axios from "axios"

export default defineComponent({
    props: {
        tableName: {
            type: String as PropType<string>,
            required: true
        },
        rowID: {
            type: undefined as unknown as PropType<RowID>,
            required: true
        }
    },
    components: {
        DeleteButton,
        DropDownMenu,
        RowForm,
        ReferencingTables,
        FormErrors
    },
    data: function () {
        return {
            errors: [] as string[],
            showDropdown: false,
            saveButtonEnabled: true
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
    setup() {
        return {
            readable
        }
    },
    methods: {
        async submitForm(event: Event) {
            console.log("Submitting...")

            this.saveButtonEnabled = false

            const form = new FormData(event.target as HTMLFormElement)

            const json: { [key: string]: any } = {}
            for (const i of form.entries()) {
                const key = i[0]
                let value = i[1]

                json[key] = convertFormValue({
                    key,
                    value,
                    schema: this.schema
                })
            }

            let config: UpdateRow = {
                tableName: this.tableName,
                rowID: this.rowID,
                data: json
            }
            try {
                await this.$store.dispatch("updateRow", config)
                var message: APIResponseMessage = {
                    contents: "Successfully saved row",
                    type: "success"
                }
                this.$store.commit("updateApiResponseMessage", message)
                this.errors = []
            } catch (error) {
                if (axios.isAxiosError(error) && error.response) {
                    this.errors = parseErrorResponse(
                        error.response.data,
                        error.response.status
                    )
                }

                window.scrollTo(0, 0)

                var message: APIResponseMessage = {
                    contents: "The form has errors.",
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)
            }

            this.saveButtonEnabled = true
        },
        async deleteRow() {
            if (window.confirm("Are you sure you want to delete this row?")) {
                let config: DeleteRow = {
                    tableName: this.tableName,
                    rowID: this.rowID
                }

                try {
                    await this.$store.dispatch("deleteRow", config)
                } catch (error) {
                    if (axios.isAxiosError(error) && error.response) {
                        this.errors = parseErrorResponse(
                            error.response.data,
                            error.response.status
                        )
                    }

                    var message: APIResponseMessage = {
                        contents: "Unable to delete the row.",
                        type: "error"
                    }
                    this.$store.commit("updateApiResponseMessage", message)

                    return
                }

                alert("Successfully deleted row")
                await this.$router.push({
                    name: "rowListing",
                    params: { tableName: this.tableName }
                })
            }
        },
        async fetchData() {
            this.$store.commit("updateCurrentTablename", this.tableName)
            await this.$store.dispatch("fetchSingleRow", {
                tableName: this.tableName,
                rowID: this.rowID
            })
        }
    },
    watch: {
        "$route.params.tableName": async function () {
            await Promise.all([
                this.fetchData(),
                this.$store.dispatch("fetchSchema", this.tableName)
            ])
        },
        "$route.params.rowID": async function () {
            await this.fetchData()
        }
    },
    async mounted() {
        await Promise.all([
            this.fetchData(),
            this.$store.dispatch("fetchSchema", this.tableName)
        ])
    }
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
