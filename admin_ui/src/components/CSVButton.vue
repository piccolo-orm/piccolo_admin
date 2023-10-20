<template>
    <a class="button" v-on:click="fetchExportedRows">
        <font-awesome-icon icon="file-csv" />
        <span>{{ $t("Export CSV") }}</span>
    </a>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"
import axios from "axios"

import type { RowCountAPIResponse } from "../interfaces"
import { getOrderByString } from "@/utils"

export default defineComponent({
    props: {
        tableName: {
            type: String as PropType<string>
        }
    },
    methods: {
        // Export data as csv from json:
        async fetchExportedRows() {
            alert(
                "Your data will begin downloading. Large data sets may take a while."
            )

            const params = this.$store.state.filterParams
            const orderBy = this.$store.state.orderBy
            if (orderBy && orderBy.length > 0) {
                params["__order"] = getOrderByString(orderBy)
            }
            // Get the row counts:
            const response = await axios.get(
                `api/tables/${this.tableName}/count/`,
                {
                    params
                }
            )
            const data = response.data as RowCountAPIResponse
            const localParams = { ...params }

            localParams["__page"] = data.count
            // Set higher __page_size param to have fewer requests to api:
            localParams["__page_size"] = 1000
            const pages = Math.ceil(data.count / localParams["__page_size"])
            const exportedRows = []

            try {
                for (let i = 1; i < pages + 1; i++) {
                    localParams["__page"] = i
                    const response = await axios.get(
                        `api/tables/${this.tableName}/?__readable=true`,
                        {
                            params: localParams
                        }
                    )
                    exportedRows.push(...response.data.rows)
                }
                let data: string = ""
                data += [
                    Object.keys(exportedRows[0]).join(";"),
                    ...exportedRows.map((item) => Object.values(item).join(";"))
                ].join("\n")
                let csv = new Blob([data], {
                    type: "text/csv;charset=utf-8;"
                })
                const url: string = URL.createObjectURL(csv)
                const link: HTMLAnchorElement = document.createElement("a")
                alert("Your data is ready.")
                link.setAttribute("href", url)
                link.setAttribute("download", `${this.tableName}.csv`)
                link.click()
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    console.log(error.response)
                }
            }
        }
    }
})
</script>

<style lang="less" scoped>
a.button {
    div {
        cursor: pointer;
    }
}
</style>
