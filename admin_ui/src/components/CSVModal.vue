<template>
    <Modal @close="$emit('close')" data-uitest="csv_modal">
        <p>{{ $t("Export CSV") }}</p>

        <form @submit.prevent="fetchExportedRows">
            <label for="delimiter">{{ $t("Delimiter") }}</label>
            <select id="delimiter" v-model="delimiter">
                <option value=",">{{ $t("Comma") }}</option>
                <option value=";">{{ $t("Semicolon") }}</option>
            </select>

            <p id="toggle_all">
                Columns<a href="#" @click.prevent="toggleAll()">Toggle all</a>
            </p>

            <ul class="column_list">
                <li v-for="columnName in Object.keys(schema.properties)">
                    <label :for="columnName">
                        {{ columnName }}
                    </label>
                    <input
                        type="checkbox"
                        :name="columnName"
                        :checked="selectedColumns.indexOf(columnName) != -1"
                        :value="columnName"
                        @change="toggleValue($event, columnName)"
                    />
                </li>
            </ul>

            <ul class="column_list">
                <li>
                    <label>Include readable</label>
                    <input type="checkbox" checked />
                </li>
            </ul>

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

// I'm not sure how to handle this ...
// I can't have a v-model for each checkbox ...

const selectedColumns = ref<string[]>([])

const toggleAll = () => {
    if (selectedColumns.value.length == 0) {
        selectedColumns.value = Object.keys(schema.value.properties)
    } else {
        selectedColumns.value = []
    }
}

const toggleValue = (event: Event, columnName: string) => {
    const checked = (event.target as HTMLInputElement).checked
    if (checked) {
        selectedColumns.value.push(columnName)
    } else {
        selectedColumns.value = selectedColumns.value.filter(
            (i) => i != columnName
        )
    }
}

onMounted(() => {
    selectedColumns.value = Object.keys(schema.value.properties)
})

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

const fetchExportedRows = async () => {
    buttonDisabled.value = true

    const params = store.state.filterParams
    const orderBy = store.state.orderBy
    const tableName = store.state.currentTableName

    if (orderBy && orderBy.length > 0) {
        params["__order"] = getOrderByString(orderBy)
    }
    // Get the row counts:
    const response = await axios.get(`api/tables/${tableName}/count/`, {
        params
    })
    const data = response.data as RowCountAPIResponse
    const localParams = { ...params }

    localParams["__page"] = data.count
    // Set higher __page_size param to have fewer requests to the API:
    localParams["__page_size"] = 1000
    const pages = Math.ceil(data.count / localParams["__page_size"])
    const exportedRows = []

    try {
        for (let i = 1; i < pages + 1; i++) {
            localParams["__page"] = i
            const response = await axios.get(
                `api/tables/${tableName}/?__readable=true`,
                {
                    params: localParams
                }
            )
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

p#toggle_all {
    a {
        text-decoration: none;
        font-size: 0.8em;
        float: right;
    }
}

ul.column_list {
    margin-left: 0;
    padding-left: 0;

    li {
        box-sizing: border-box;
        padding: 0.5rem;
        list-style: none;
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

        &:nth-child(odd) {
            background-color: rgba(0, 0, 0, 0.2);
        }
    }
}
</style>
