<template>
    <Modal @close="$emit('close')" data-uitest="csv_modal">
        <p>{{ $t("Export CSV") }}</p>

        <form @submit.prevent="fetchExportedRows">
            <label for="delimiter">{{ $t("Delimiter") }}</label>
            <select id="delimiter" v-model="delimiter">
                <option value=",">{{ $t("Comma") }}</option>
                <option value=";">{{ $t("Semicolon") }}</option>
            </select>

            <p id="column_header">
                <a href="#" @click.prevent="showColumnTable = !showColumnTable">
                    <font-awesome-icon
                        :icon="showColumnTable ? 'angle-down' : 'angle-right'"
                    />
                    Columns</a
                ><a
                    id="toggle_all"
                    href="#"
                    @click.prevent="toggleAll()"
                    v-show="showColumnTable"
                    >Toggle all</a
                >
            </p>

            <table class="column_list" v-show="showColumnTable">
                <tbody>
                    <tr v-for="columnName in allColumnNames">
                        <td>
                            <label :for="'csv_' + columnName">{{
                                columnName
                            }}</label>

                            <input
                                type="checkbox"
                                :id="'csv_' + columnName"
                                :checked="
                                    selectedColumns.indexOf(columnName) != -1
                                "
                                @change="
                                    toggleValue(
                                        ($event.target as HTMLInputElement)
                                            .checked,
                                        columnName
                                    )
                                "
                            />
                        </td>
                    </tr>
                </tbody>

                <tfoot>
                    <tr>
                        <td>
                            <label for="include_readable"
                                >Include readable</label
                            >
                            <input
                                type="checkbox"
                                id="include_readable"
                                v-model="includeReadable"
                            />
                        </td>
                    </tr>
                </tfoot>
            </table>

            <button
                data-uitest="download_csv_button"
                :disabled="buttonDisabled"
            >
                <font-awesome-icon icon="download" />
                <span>{{ $t("Download") }}</span>
            </button>

            <!-- prettier-ignore -->
            <p class="note">{{ $t("Note: Large data sets may take a while.") }}</p>
        </form>
    </Modal>
</template>

<script setup lang="ts">
import axios from "axios"
import { ref, inject, computed, onMounted, watch } from "vue"
import type { I18n } from "vue-i18n"

import type { RowCountAPIResponse, Schema } from "../interfaces"
import { getOrderByString } from "@/utils"
import Modal from "./Modal.vue"
import { useStore } from "vuex"

/*****************************************************************************/

const store = useStore()
const emit = defineEmits(["close"])

const buttonDisabled = ref<boolean>(false)
const delimiter = ref<"," | ";">(",")
const i18n = inject<I18n>("i18n")

/*****************************************************************************/

const schema = computed((): Schema => {
    return store.state.schema
})

/*****************************************************************************/

const showColumnTable = ref<boolean>(false)

/*****************************************************************************/

const selectedColumns = ref<string[]>([])
const includeReadable = ref<boolean>(true)

const toggleAll = () => {
    if (selectedColumns.value.length == 0) {
        selectedColumns.value = allColumnNames.value
    } else {
        selectedColumns.value = []
    }
}

const toggleValue = (checked: boolean, columnName: string) => {
    if (checked) {
        selectedColumns.value.push(columnName)
    } else {
        selectedColumns.value = selectedColumns.value.filter(
            (i) => i != columnName
        )
    }
}

const allColumnNames = computed(() => {
    let columnNames = Object.keys(schema.value.properties)
    const primaryKeyName = schema.value.extra.primary_key_name

    if (columnNames.indexOf(primaryKeyName) == -1) {
        columnNames = [primaryKeyName, ...columnNames]
    }

    return columnNames
})

const setupInitialColumns = () => {
    selectedColumns.value = schema.value.extra.visible_column_names
}

watch(schema, setupInitialColumns)

onMounted(setupInitialColumns)

/*****************************************************************************/

// Just in case `replaceAll` isn't supported by the browser, provide a
// fallback.
const replaceAll = (input: string, value: string, newValue: string): string => {
    if (String.prototype.replaceAll != undefined) {
        return input.replaceAll(value, newValue)
    } else {
        return input.split(value).join(newValue)
    }
}

/*****************************************************************************/

// Access i18n outside of a HTML template
const translate = (term: string): string => {
    // @ts-ignore
    return i18n ? i18n.global.t(term) : term
}

/*****************************************************************************/

// We allow the user to download more than this number of rows, but we ask them
// to confirm first.
const softRowLimit = 10000

const fetchExportedRows = async () => {
    buttonDisabled.value = true

    const params = store.state.filterParams
    const tableName = store.state.currentTableName

    /*************************************************************************/
    // Get the row count

    const response = await axios.get(`api/tables/${tableName}/count/`, {
        params
    })
    const data = response.data as RowCountAPIResponse
    const rowCount = data.count

    if (
        rowCount > softRowLimit &&
        !confirm(
            `There are more than ${softRowLimit}, are you sure you want to continue?`
        )
    ) {
        return
    }

    /*************************************************************************/
    // Work out how many requests we need to make (based on the row count).
    // If there are lots of rows, we need to make multiple requests.

    const localParams = { ...params }

    // Set higher __page_size param to have fewer requests to the API:
    localParams["__page_size"] = 1000

    const pages = Math.ceil(rowCount / localParams["__page_size"])

    /*************************************************************************/
    // Make sure orderBy is included in the query, so it matches how the
    // results are currently displayed.

    const orderBy = store.state.orderBy

    if (orderBy && orderBy.length > 0) {
        localParams["__order"] = getOrderByString(orderBy)
    }

    /*************************************************************************/
    // Work out which columns to fetch

    if (selectedColumns.value.length == 0) {
        alert("Please select at least one column.")
        return
    }

    if (selectedColumns.value.length != allColumnNames.value.length) {
        // If only some columns are selected, we need to filter which are
        // returned.
        localParams["__visible_fields"] = selectedColumns.value.join(",")
    }

    /*************************************************************************/
    // Add readable if required

    localParams["__readable"] = true

    /*************************************************************************/

    const exportedRows = []

    try {
        for (let i = 1; i < pages + 1; i++) {
            localParams["__page"] = i
            const response = await axios.get(`api/tables/${tableName}/`, {
                params: localParams
            })
            exportedRows.push(...response.data.rows)
        }
        let data: string = ""
        data += [
            Object.keys(exportedRows[0]).join(delimiter.value),
            ...exportedRows.map((item) =>
                Object.values(item)
                    .map((i) => `"${replaceAll(String(i), '"', '""')}"`)
                    .join(delimiter.value)
            )
        ].join("\n")
        let csv = new Blob([data], {
            type: "text/csv;charset=utf-8;"
        })
        const url: string = URL.createObjectURL(csv)
        const link: HTMLAnchorElement = document.createElement("a")
        link.setAttribute("href", url)
        link.setAttribute("download", `${tableName}.csv`)
        link.click()
        store.commit("updateApiResponseMessage", {
            contents: translate("Download successful"),
            type: "success"
        })
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.log(error.response)
        }
        store.commit("updateApiResponseMessage", {
            contents: translate("Download failed"),
            type: "error"
        })
    }

    buttonDisabled.value = false
    emit("close")
}
</script>

<style lang="less">
p.note {
    font-size: 0.85em;
}

p#column_header {
    margin-bottom: 0;

    a {
        text-decoration: none;

        &#toggle_all {
            text-decoration: none;
            font-size: 0.8em;
            float: right;
        }
    }
}

table.column_list {
    width: 100%;

    tr {
        td {
            box-sizing: border-box;
            padding: 0.5rem;
            display: flex;
            flex-direction: row;

            label {
                flex-grow: 1;
                padding: 0;
            }

            input {
                flex-grow: 0;
            }

            a {
                text-decoration: none;
            }
        }
    }

    tfoot {
        td {
            margin-top: 1rem;
        }
    }
}
</style>
