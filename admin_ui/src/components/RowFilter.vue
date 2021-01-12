<template>
    <div class="filter_wrapper">
        <h1>Filter</h1>

        <a
            @click="closeSideBar()"
            class="button"
            id="sidebar-close"
        >
            <span>
                <font-awesome-icon icon="times" />
            </span>Close
        </a>

        <form
            ref="form"
            v-on:submit.prevent="submitForm($event)"
        >
            <RowForm
                v-bind:isFilter="true"
                v-bind:schema="schema"
            />
            <button>Apply</button>
        </form>
        <button v-on:click.prevent="clearFilters">Clear filters</button>
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import RowForm from "./RowForm.vue"
import { APIResponseMessage } from "../interfaces"

export default Vue.extend({
    props: {
        showFilterSidebar: Boolean,
    },
    components: {
        RowForm,
    },
    computed: {
        schema() {
            return this.$store.state.schema
        },
        tableName() {
            return this.$store.state.currentTableName
        },
    },
    methods: {
        closeSideBar() {
            this.$emit("closeSideBar", false)
        },
        showSuccess(contents: string) {
            var message: APIResponseMessage = {
                contents: contents,
                type: "success",
            }
            this.$store.commit("updateApiResponseMessage", message)
        },
        async submitForm(event: any) {
            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                if (i[1] && i[1] != "all") {
                    json[i[0].split(" ").join("_")] = i[1]
                }
            }

            this.$store.commit("updateFilterParams", json)
            this.$store.commit("updateCurrentPageNumber", 1)

            try {
                await this.$store.dispatch("fetchRows")
            } catch (error) {
                return
            }
            this.showSuccess("Successfully applied filter")
        },
        async clearFilters() {
            console.log("Clearing ...")
            let form: HTMLFormElement = this.$refs.form
            form.reset()
            this.$store.commit("updateFilterParams", {})
            this.$store.commit("updateCurrentPageNumber", 1)
            try {
                await this.$store.dispatch("fetchRows")
            } catch (error) {
                return
            }
            this.showSuccess("Successfully cleared filters")
        },
    },
})
</script>


<style scoped lang="less">
div.filter_wrapper {
    position: relative;

    #sidebar-close {
        cursor: pointer;
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
    }
}
</style>
