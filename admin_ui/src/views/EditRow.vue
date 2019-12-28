<template>
    <div>
        <NavBar />
        <div
            class="edit_wrapper"
            v-if="schema"
        >
            <p>
                <a
                    href="#"
                    v-on:click.prevent="$router.go(-1)"
                >Back</a>
            </p>

            <h1>Edit</h1>

            <pre>{{ errors }}</pre>

            <form v-on:submit.prevent="submitForm($event)">
                <RowForm
                    v-bind:row="selectedRow"
                    v-bind:schema="schema"
                />
                <button>Save</button>
            </form>
        </div>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import NavBar from "../components/NavBar.vue"
import RowForm from "../components/RowForm.vue"
import { UpdateRow } from "../interfaces"

export default Vue.extend({
    props: ["tableName", "rowID"],
    components: {
        RowForm,
        NavBar
    },
    data: function() {
        return {
            errors: ""
        }
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
        async submitForm(event) {
            console.log("Submitting...")

            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                json[i[0].split(" ").join("_")] = i[1]
            }

            let config: UpdateRow = {
                tableName: this.tableName,
                rowID: this.rowID,
                data: json
            }
            try {
                await this.$store.dispatch("updateRow", config)
            } catch (error) {
                this.errors = error.response.data
                return
            }
            this.errors = ""
        }
    },
    async mounted() {
        this.$store.commit("updateCurrentTablename", this.tableName)
        await Promise.all([
            this.$store.dispatch("fetchSingleRow", {
                tableName: this.tableName,
                rowID: this.rowID
            }),
            this.$store.dispatch("fetchSchema", this.tableName)
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
