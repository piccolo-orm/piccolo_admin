<template>
    <a class="button">
        <downloadexcel
            :before-finish="finishDownload"
            :before-generate="startDownload"
            :fetch="fetchExportedRows"
            :name="tableName + '.csv'"
            type="csv"
        >
            <font-awesome-icon icon="file-csv" />
            <span>{{ $t("Export CSV") }}</span>
        </downloadexcel>
    </a>
</template>

<script lang="ts">
import axios from "axios"
import downloadexcel from "vue-json-excel"
import * as i from "../interfaces"

export default {
    props: ["tableName"],
    components: {
        downloadexcel
    },
    methods: {
        // Export data as csv from json:
        async fetchExportedRows() {
            const params = this.$store.state.filterParams
            const orderBy = this.$store.state.orderBy
            if (orderBy) {
                let prefix = orderBy.ascending ? "" : "-"
                params["__order"] = prefix + orderBy.property
            }
            // Get the row counts:
            const response = await axios.get(
                `api/tables/${this.tableName}/count/`,
                {
                    params
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
                            params: localParams
                        }
                    )
                    exportedRows.push(...response.data.rows)
                }
                return exportedRows
            } catch (error) {
                console.log(error.response)
            }
        },
        startDownload() {
            alert(
                "Your data will begin downloading. Large data sets may take a few seconds."
            )
        },
        finishDownload() {
            alert("Your data is ready.")
        }
    }
}
</script>

<style lang="less" scoped>
a.button {
    div {
        cursor: pointer;
    }
}
</style>
