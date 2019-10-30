<template>
    <div>
        <h1>Filter</h1>

        <form
            ref="form"
            v-on:submit.prevent="submitForm($event)"
        >
            <div
                v-bind:key="field.title"
                v-for="field in schema.properties"
            >
                <label>{{ field.title }}</label>
                <input
                    type="number"
                    v-bind:name="field.title.toLowerCase()"
                    v-if="field.type == 'integer'"
                />
                <input
                    type="text"
                    v-bind:name="field.title.toLowerCase()"
                    v-if="field.type == 'string'"
                />
                <input
                    type="checkbox"
                    v-bind:name="field.title.toLowerCase()"
                    v-if="field.type == 'boolean'"
                />
            </div>
            <button>Apply</button>
        </form>
        <button v-on:click.prevent="clearFilters">Clear filters</button>
    </div>
</template>


<script lang="ts">
import Vue from "vue"

export default Vue.extend({
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
                json[i[0]] = i[1]
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
