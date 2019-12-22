<template>
    <div>
        <h1>Filter</h1>

        <form
            ref="form"
            v-on:submit.prevent="submitForm($event)"
        >
            <RowForm v-bind:schema="schema" v-bind:isFilter="true" />
            <button>Apply</button>
        </form>
        <button v-on:click.prevent="clearFilters">Clear filters</button>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import RowForm from "./RowForm.vue"
import {APIResponseMessage} from "../interfaces"

export default Vue.extend({
    components: {
        RowForm
    },
    computed: {
        schema() {
            return this.$store.state.schema
        },
        tableName() {
            return this.$store.state.currentTableName
        }
    },
    methods: {
        showSuccess(contents: string) {
            var message: APIResponseMessage = {
                contents: contents,
                type: 'success'
            }
            this.$store.commit('updateApiResponseMessage', message)
        },
        async submitForm(event: any) {
            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {

                if (i[1] && i[1] != 'all') {
                    json[i[0].replace(" ", "_")] = i[1]
                }
            }
            try {
                await this.$store.dispatch("fetchRows", {
                    tableName: this.tableName,
                    params: json
                })
            } catch(error) {
                return
            }
            this.showSuccess('Successfully applied filter')
        },
        async clearFilters() {
            console.log("Clearing ...")
            let form: HTMLFormElement = this.$refs.form
            form.reset()
            try {
                await this.$store.dispatch("fetchRows", {
                    tableName: this.tableName,
                    params: {}
                })
            } catch(error) {
                return
            }
            this.showSuccess('Successfully cleared filters')
        }
    }
})
</script>


<style scoped lang="less">
</style>
