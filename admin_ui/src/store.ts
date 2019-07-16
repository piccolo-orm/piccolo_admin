import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';
import * as i from './interfaces';

Vue.use(Vuex);

const BASE_URL = process.env.VUE_APP_BASE_URI


export default new Vuex.Store({
    state: {
        tableNames: [],
        currentTableName: undefined,
        rows: [],
        schema: {},
        selectedRow: undefined,
        apiResponseMessage: null as i.APIResponseMessage|null
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
        }
    },
    actions: {
        async fetchTableNames(context) {
            const response = await axios.get(`${BASE_URL}tables/`)
            this.commit('updateTableNames', response.data)
        },
        async fetchRows(context, config: i.FetchRowsConfig) {
            try {
                const response = await axios.get(
                    `${BASE_URL}tables/${config.tableName}/`,
                    {
                        params: config.params
                    }
                )
                context.commit('updateRows', response.data)
                return response
            } catch (error) {
                console.log(error)
                context.commit(
                    'updateApiResponseMessage',
                    {
                        contents: `Problem fetching ${config.tableName} rows.`,
                        type: 'error'
                    }
                )
            }
        },
        async fetchSingleRow(context, config: i.FetchSingleRowConfig) {
            const response = await axios.get(
                `${BASE_URL}tables/${config.tableName}/${config.rowID}`
            )
            context.commit('updateSelectedRow', response.data)
            return response
        },
        async fetchSchema(context, tableName: string) {
            const response =  await axios.get(
                `${BASE_URL}tables/${tableName}/schema/`
            )
            context.commit('updateSchema', response.data)
            return response
        },
        async createRow(context, config: i.CreateRow) {
            const response =  await axios.post(
                `${BASE_URL}tables/${config.tableName}/`,
                config.data
            )
            return response
        },
        async deleteRow(context, config: i.DeleteRow) {
            const response =  await axios.delete(
                `${BASE_URL}tables/${config.tableName}/${config.rowID}/`
            )
            return response
        },
        async updateRow(context, config: i.UpdateRow) {
            const response = await axios.put(
                `${BASE_URL}tables/${config.tableName}/${config.rowID}/`,
                config.data
            )

            context.commit(
                'updateApiResponseMessage',
                {
                    contents: 'Successfully saved row',
                    type: 'success'
                }
            )

            return response
        }
    },
});
