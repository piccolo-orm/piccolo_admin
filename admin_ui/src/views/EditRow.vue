<template>
<div>
    <NavBar />
    <div class="edit_wrapper">
        <p>
            <a href='#' v-on:click.prevent="$router.go(-1)">Back</a>
        </p>

        <h1>Edit</h1>

        <form v-on:submit.prevent="submitForm($event)">
            <div v-for="property in schema.properties" v-bind:key="property.title">
                <label>{{ property.title }}</label>

                <template v-if="property.foreign_key">
                    <KeySelect
                        v-bind:tableName="property.to"
                        v-bind:fieldName="property.title.toLowerCase()" />
                </template>
                <template v-else>
                    <input
                        type="text"
                        v-bind:name="property.title.toLowerCase()"
                        v-bind:value="getValue(property.title)">
                </template>

            </div>
            <button>Save</button>
        </form>
    </div>
</div>
</template>


<script lang="ts">
import Vue from 'vue'
import NavBar from '../components/NavBar.vue'
import KeySelect from '../components/KeySelect.vue'
import {UpdateRow} from '../interfaces'


export default Vue.extend({
    props: [
        'tableName',
        'rowID'
    ],
    components: {
        NavBar,
        KeySelect
    },
    computed: {
        schema() {
            return this.$store.state.schema
        },
        selectedRow() {
            return this.$store.state.selectedRow
        }
    },
    methods: {
        getValue(value) {
            return this.selectedRow ? this.selectedRow[value.toLowerCase()] : ''
        },
        async submitForm(event) {
            console.log("Submitting...")

            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                json[i[0]] = i[1]
            }

            let config: UpdateRow = {
                tableName: this.tableName,
                rowID: this.rowID,
                data: json
            }
            this.$store.dispatch('updateRow', config)
        }
    },
    async mounted() {
        this.$store.commit('updateCurrentTablename', this.tableName)
        await Promise.all([
            this.$store.dispatch(
                'fetchSingleRow',
                {
                    tableName: this.tableName,
                    rowID: this.rowID
                }
            ),
            this.$store.dispatch('fetchSchema', this.tableName)
        ])
    }
})
</script>


<style lang="less">
div.edit_wrapper {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;

    h1 {
        margin: 0;
    }
}
</style>
