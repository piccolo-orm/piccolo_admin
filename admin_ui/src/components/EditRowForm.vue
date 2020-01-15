<template>
    <div v-if="schema">
        <h1>Edit {{ tableName }}</h1>

        <pre>{{ errors }}</pre>

        <form v-on:submit.prevent="submitForm($event)">
            <RowForm
                :row="selectedRow"
                :schema="schema"
            />
            <button>Save</button>
        </form>

        <div class="action_wrapper">
            <ReferencingTables
                :rowID="rowID"
                :tableName="tableName"
            />
            <p id="delete">
                <DeleteButton
                    class="subtle"
                    v-on:triggered="deleteRow"
                />
            </p>
        </div>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import ReferencingTables from "../components/ReferencingTables.vue"
import DeleteButton from "./DeleteButton.vue"
import RowForm from "./RowForm.vue"
import { UpdateRow, DeleteRow } from "../interfaces"

export default Vue.extend({
    props: ["tableName", "rowID"],
    components: {
        DeleteButton,
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
        },
        async deleteRow() {
            if (window.confirm("Are you sure you want to delete this row?")) {
                let config: DeleteRow = {
                    tableName: this.tableName,
                    rowID: this.rowID
                }
                await this.$store.dispatch("deleteRow", config)
                alert("Successfully deleted row")
                this.$router.push({
                    name: "rowListing",
                    params: { tableName: this.tableName }
                })
            }
        },
        async fetchData() {
            this.$store.commit("updateCurrentTablename", this.tableName)
            await this.$store.dispatch("fetchSingleRow", {
                tableName: this.tableName,
                rowID: this.rowID
            })
        }
    },
    watch: {
        "$route.params.tableName": async function() {
            await Promise.all([
                this.fetchData(),
                this.$store.dispatch("fetchSchema", this.tableName)
            ])
        },
        "$route.params.rowID": async function() {
            await this.fetchData()
        }
    },
    async mounted() {
        await Promise.all([
            this.fetchData(),
            this.$store.dispatch("fetchSchema", this.tableName)
        ])
    }
})
</script>


<style scoped lang="less">
h1 {
    text-transform: capitalize;
}

div.action_wrapper {
    display: flex;
    flex-direction: row;

    div,
    p#delete {
        flex: 50%;
    }

    p#delete {
        text-align: right;

        a {
            font-size: 0.8rem;
        }
    }
}
</style>
