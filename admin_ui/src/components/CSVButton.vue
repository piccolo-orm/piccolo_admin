<template>
    <a
        class="button"
        v-on:click="fetchExportedRows"
    >
        <font-awesome-icon icon="file-csv" />
        <span>Export CSV</span>
    </a>
</template>

<script lang="ts">
import axios from "axios"
import * as i from "../interfaces"

export default {
    props: ["tableName"],
    methods: {
        // Export data as csv from json:
        async fetchExportedRows() {
            alert(
                "Your data will begin downloading. Large data sets may take a while."
            )
            const params = this.$store.state.filterParams
            const sortBy = this.$store.state.sortBy
            if (sortBy) {
                let prefix = sortBy.ascending ? "" : "-"
                params["__order"] = prefix + sortBy.property
            }
            // Get the row counts:
            const response = await axios.get(
                `api/tables/${this.tableName}/count/`,
                {
                    params,
                }
            )
            const data = response.data as i.RowCountAPIResponse
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
                            params: localParams,
                        }
                    )
                    exportedRows.push(...response.data.rows)
                }
                let csv = "data:text/csv;charset=utf-8,"
                csv += [
                    Object.keys(exportedRows[0]).join(";"),
                    ...exportedRows.map((item) =>
                        Object.values(item).join(";")
                    ),
                ]
                    .join("\n")
                    .replace(/(^\[)|(\]$)/gm, "")
                const data = encodeURI(csv)
                const link = document.createElement("a")
                link.setAttribute("href", data)
                link.setAttribute("download", `${this.tableName}.csv`)
                link.click()
                alert("Your data is ready.")
            } catch (error) {
                console.log(error.response)
            }
        },
    },
}
</script>

<style lang="less" scoped>
a.button {
    div {
        cursor: pointer;
    }
}
</style>