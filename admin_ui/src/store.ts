import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import * as i from './interfaces'

Vue.use(Vuex)

const BASE_URL = process.env.VUE_APP_BASE_URI

export default new Vuex.Store({
    state: {
        tableNames: [],
        currentTableName: undefined,
        rows: [],
        schema: undefined,
        selectedRow: undefined,
        apiResponseMessage: null as i.APIResponseMessage | null,
        user: undefined,
        sortBy: null as i.SortByConfig | null,
        filterParams: {},
        rowCount: 0,
        pageSize: 1,
        currentPageNumber: 1
    },
    mutations: {
        updateTableNames(state, value) {
            state.tableNames = value
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
        updateApiResponseMessage(state, message: i.APIResponseMessage) {
            state.apiResponseMessage = message
        },
        updateUser(state, user) {
            state.user = user
        },
        updateSortBy(state, config: i.SortByConfig) {
            state.sortBy = config
        },
        reset(state) {
            state.sortBy = null
            state.filterParams = {}
            state.currentPageNumber = 1
            state.rows = []
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
        }
    },
    actions: {
        async fetchTableNames(context) {
            const response = await axios.get(`${BASE_URL}tables/`)
            this.commit('updateTableNames', response.data)
        },
        async fetchRows(context) {
            const params = context.state.filterParams
            const tableName = context.state.currentTableName

            const sortBy = context.state.sortBy
            if (sortBy) {
                let prefix = sortBy.ascending ? '' : '-'
                params['__order'] = prefix + sortBy.property
            }

            // Get the row counts:
            const response = await axios.get(
                `${BASE_URL}tables/${tableName}/count/`,
                {
                    params
                }
            )
            const data = response.data as i.RowCountAPIResponse
            context.commit('updateRowCount', data.count)
            context.commit('updatePageSize', data.page_size)
            if (data.count < data.page_size) {
                context.commit('updateCurrentPageNumber', 1)
            }

            params['__page'] = context.state.currentPageNumber

            try {
                const response = await axios.get(
                    `${BASE_URL}tables/${tableName}/?__readable=true`,
                    {
                        params: params
                    }
                )
                context.commit('updateRows', response.data.rows)
            } catch (error) {
                console.log(error.response)
                context.commit('updateApiResponseMessage', {
                    contents: `Problem fetching ${tableName} rows.`,
                    type: 'error'
                })
            }
        },
        async fetchIds(context, tableName: string) {
            const response = await axios.get(
                `${BASE_URL}tables/${tableName}/ids/`
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
                `${BASE_URL}tables/${config.tableName}/${config.rowID}/`
            )
            context.commit('updateSelectedRow', response.data)
            return response
        },
        async fetchSchema(context, tableName: string) {
            const response = await axios.get(
                `${BASE_URL}tables/${tableName}/schema/`
            )
            context.commit('updateSchema', response.data)
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
            const response = await axios.put(
                `${BASE_URL}tables/${config.tableName}/${config.rowID}/`,
                config.data
            )

            context.commit('updateApiResponseMessage', {
                contents: 'Successfully saved row',
                type: 'success'
            })

            return response
        }
    }
})
