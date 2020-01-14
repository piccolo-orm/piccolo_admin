<template>
    <div v-if="schema">
        <h1>Edit</h1>

        <pre>{{ errors }}</pre>

        <form v-on:submit.prevent="submitForm($event)">
            <RowForm
                :row="selectedRow"
                :schema="schema"
            />
            <button>Save</button>
        </form>

        <ReferencingTables
            :rowID="rowID"
            :tableName="tableName"
        />
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import ReferencingTables from "../components/ReferencingTables.vue"
import RowForm from "../components/RowForm.vue"
import { UpdateRow } from "../interfaces"

export default Vue.extend({
    props: ["tableName", "rowID"],
    components: {
        RowForm,
        ReferencingTables
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


<style scoped lang="less">
@import "../vars.less";

div.edit_wrapper {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;

    a {
        text-decoration: none;
    }

    h1 {
        margin: 0;
    }

    p.referencing_title {
        color: @border_color;
        font-size: 0.8rem;
        margin-top: 1rem;
        padding: 0.5rem 0;
    }

    ul.related_tables {
        li {
            span.table {
                font-weight: bold;
                text-transform: capitalize;
            }
        }
    }
}
</style>
