<template>
    <div>
        <h1>Filter</h1>

        <form
            ref="form"
            v-on:submit.prevent="submitForm($event)"
        >
            <RowForm v-bind:schema="schema" />
            <button>Apply</button>
        </form>
        <button v-on:click.prevent="clearFilters">Clear filters</button>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import RowForm from "./RowForm.vue"

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
        async submitForm(event: any) {
            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                if (i[1]) {
                    json[i[0].replace(" ", "_")] = i[1]
                }
            }
            await this.$store.dispatch("fetchRows", {
                tableName: this.tableName,
                params: json
            })
        },
        async clearFilters() {
            console.log("Clearing ...")
            let form: HTMLFormElement = this.$refs.form
            form.reset()
            await this.$store.dispatch("fetchRows", {
                tableName: this.tableName,
                params: {}
            })
        }
    }
})
</script>


<style scoped lang="less">
</style>
