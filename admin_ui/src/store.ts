import Vue from "vue"
import Vuex from "vuex"
import axios from "axios"

import * as i from "./interfaces"
import aboutModalModule from "./modules/aboutModal"
import metaModule from "./modules/meta"
import translationsModule from "./modules/translations"
import { getOrderByString } from "./utils"

Vue.use(Vuex)

const BASE_URL = process.env.VUE_APP_BASE_URI

export default new Vuex.Store({
    modules: {
        aboutModalModule,
        metaModule,
        translationsModule
    },
    state: {
        apiResponseMessage: null as i.APIResponseMessage | null,
        currentPageNumber: 1,
        currentTableName: undefined,
        darkMode: false,
        filterParams: {},
        pageSize: 15,
        rowCount: 0,
        rows: [],
        schema: undefined as i.Schema | undefined,
        formSchema: undefined,
        selectedRow: undefined,
        orderBy: null as i.OrderByConfig[] | null,
        tableNames: [],
        tableGroups: {},
        formConfigs: [] as i.FormConfig[],
        chartConfigs: [] as i.ChartConfig[],
        user: undefined,
        loadingStatus: false,
        customLinks: {}
    },
    mutations: {
        updateTableGroups(state, value) {
            state.tableGroups = value
        },
        updateTableNames(state, value) {
            state.tableNames = value
        },
        updateFormConfigs(state, value) {
            state.formConfigs = value
        },
        updateCurrentTablename(state, value) {
            state.currentTableName = value
        },
        updateRows(state, rows) {
            state.rows = rows
        },
        updateSelectedRow(state, row) {
            state.selectedRow = row
        },
        updateSchema(state, schema) {
            state.schema = schema
        },
        updateFormSchema(state, formSchema) {
            state.formSchema = formSchema
        },
        updateChartConfigs(state, value) {
            state.chartConfigs = value
        },
        updateApiResponseMessage(state, message: i.APIResponseMessage) {
            state.apiResponseMessage = message
        },
        updateUser(state, user) {
            state.user = user
        },
        updateOrderBy(state, config: i.OrderByConfig[]) {
            state.orderBy = config
        },
        reset(state) {
            state.orderBy = null
            state.filterParams = {}
            state.currentPageNumber = 1
            state.rows = null
        },
        updateFilterParams(state, config: object) {
            state.filterParams = config
        },
        updateRowCount(state, rowCount: number) {
            state.rowCount = rowCount
        },
        updatePageSize(state, pageSize: number) {
            state.pageSize = pageSize
        },
        updateCurrentPageNumber(state, pageNumber: number) {
            state.currentPageNumber = pageNumber
        },
        updateDarkMode(state, enabled: boolean) {
            state.darkMode = enabled
            localStorage.setItem("darkMode", String(enabled))
        },
        updateLoadingStatus(state, value) {
            state.loadingStatus = value
        },
        updateCustomLinks(state, value) {
            state.customLinks = value
        }
    },
    actions: {
        async fetchFormConfigs(context) {
            const response = await axios.get(`${BASE_URL}forms/`)
            context.commit("updateFormConfigs", response.data)
        },
        async fetchFormConfig(context, formSlug: string) {
            return await axios.get(`${BASE_URL}forms/${formSlug}/`)
        },
        async fetchFormSchema(context, formSlug: string) {
            const response = await axios.get(
                `${BASE_URL}forms/${formSlug}/schema/`
            )
            context.commit("updateFormSchema", response.data)
            return response
        },
        async fetchChartConfigs(context) {
            const response = await axios.get(`${BASE_URL}charts/`)
            context.commit("updateChartConfigs", response.data)
        },
        async fetchChartConfig(context, chartSlug: string) {
            return await axios.get(`${BASE_URL}charts/${chartSlug}/`)
        },
        async fetchChartData(
            context,
            config: { chartSlug: string; data: object }
        ) {
            return await axios.post(
                `${BASE_URL}charts/${config.chartSlug}/data/`,
                config.data
            )
        },
        async fetchChartSchema(context, chartSlug: string) {
            return await axios.get(`${BASE_URL}charts/${chartSlug}/schema/`)
        },

        /*********************************************************************/

        async fetchTableNames(context) {
            const response = await axios.get(`${BASE_URL}tables/`)
            context.commit("updateTableNames", response.data)
        },
        async fetchTableGroups(context) {
            const response = await axios.get(`${BASE_URL}tables/grouped/`)
            context.commit("updateTableGroups", response.data)
        },
        async fetchCustomLinks(context) {
            const response = await axios.get(`${BASE_URL}links/`)
            context.commit("updateCustomLinks", response.data)
        },
        async fetchCount(context) {
            const tableName = context.state.currentTableName
            const params = context.state.filterParams
            const response = await axios.get(
                `${BASE_URL}tables/${tableName}/count/`,
                {
                    params
                }
            )
            const data = response.data as i.RowCountAPIResponse
            context.commit("updateRowCount", data.count)
            return data
        },
        async fetchRows(context) {
            context.commit("updateLoadingStatus", true)
            const params = context.state.filterParams
            const tableName = context.state.currentTableName

            const orderByConfigs = context.state.orderBy
            if (orderByConfigs) {
                params["__order"] = getOrderByString(orderByConfigs)
            }

            // Get the row counts:
            const rowCountResponse = await context.dispatch("fetchCount")
            params["__page_size"] = context.state.pageSize

            if (rowCountResponse.count < params["__page_size"]) {
                context.commit("updateCurrentPageNumber", 1)
            }

            // Now get the rows:
            params["__page"] = context.state.currentPageNumber

            try {
                const response = await axios.get(
                    `${BASE_URL}tables/${tableName}/?__readable=true`,
                    {
                        params: params
                    }
                )
                context.commit("updateRows", response.data.rows)
            } catch (error) {
                console.log(error.response)
                context.commit("updateApiResponseMessage", {
                    contents: `Problem fetching ${tableName} rows.`,
                    type: "error"
                })
            }
            context.commit("updateLoadingStatus", false)
        },
        async fetchTableReferences(context, tableName: string) {
            const response = await axios.get(
                `${BASE_URL}tables/${tableName}/references/`
            )
            return response
        },
        async fetchIds(context, config: i.FetchIdsConfig) {
            const params = {}

            if (config.search) {
                params["search"] = config.search
            }

            if (config.limit) {
                params["limit"] = config.limit
            }

            if (config.offset) {
                params["offset"] = config.offset
            }

            const response = await axios.get(
                `${BASE_URL}tables/${config.tableName}/ids/`,
                {
                    params
                }
            )
            return response
        },
        async getNew(context, tableName: string) {
            const response = await axios.get(
                `${BASE_URL}tables/${tableName}/new/`
            )
            return response
        },
        async fetchSingleRow(context, config: i.FetchSingleRowConfig) {
            const response = await axios.get(
                `${BASE_URL}tables/${config.tableName}/${config.rowID}/?__readable=true`
            )
            context.commit("updateSelectedRow", response.data)
            return response
        },
        async fetchSchema(context, tableName: string) {
            const response = await axios.get<i.Schema>(
                `${BASE_URL}tables/${tableName}/schema/`
            )
            context.commit("updateSchema", response.data)

            return response
        },
        async createRow(context, config: i.CreateRow) {
            const response = await axios.post(
                `${BASE_URL}tables/${config.tableName}/`,
                config.data
            )
            return response
        },
        async deleteRow(context, config: i.DeleteRow) {
            const response = await axios.delete(
                `${BASE_URL}tables/${config.tableName}/${config.rowID}/`
            )
            return response
        },
        async updateRow(context, config: i.UpdateRow) {
            const response = await axios.patch(
                `${BASE_URL}tables/${config.tableName}/${config.rowID}/`,
                config.data
            )
            return response
        },
        async fetchUser(context) {
            const response = await axios.get(`${BASE_URL}user/`)
            context.commit("updateUser", response.data)
        }
    }
})
