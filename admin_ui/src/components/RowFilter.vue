<template>
    <div class="filter_wrapper">
        <h1>{{ $t("Filter") }}</h1>

        <a v-on:click="closeSideBar()" class="button" id="sidebar-close">
            <span> <font-awesome-icon icon="times" /> </span>{{ $t("Close") }}
        </a>

        <form ref="form" v-on:submit.prevent="submitForm($event)">
            <FilterForm v-bind:schema="schema" />
            <button>{{ $t("Apply") }}</button>
        </form>
        <button v-on:click.prevent="clearFilters">
            {{ $t("Clear filters") }}
        </button>
    </div>
</template>

<script lang="ts">
import Vue from "vue"
import FilterForm from "./FilterForm.vue"
import { APIResponseMessage } from "../interfaces"

export default Vue.extend({
    props: {
        showFilterSidebar: Boolean
    },
    components: {
        FilterForm
    },
    computed: {
        schema() {
            return this.$store.state.schema
        }
    },
    methods: {
        closeSideBar() {
            this.$emit("closeSideBar", false)
        },
        showSuccess(contents: string) {
            var message: APIResponseMessage = {
                contents: contents,
                type: "success"
            }
            this.$store.commit("updateApiResponseMessage", message)
        },
        async submitForm(event: any) {
            const form = new FormData(event.target)

            const json = {}
            for (const i of form.entries()) {
                const key = i[0]
                let value: any = i[1]

                if (value && value != "all") {
                    if (this.schema.properties[key]?.type == "array") {
                        // @ts-ignore
                        value = JSON.parse(value).filter((i) => i)
                        // Ignore any empty values.
                        value = Array.isArray(value)
                            ? value.filter((i) => i)
                            : value
                    }

                    json[key] = value
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
            let form: any = this.$refs.form
            let _ = [...form.elements].forEach((element) => {
                if (element.type == "hidden") {
                    element.value = ""
                }
            })

            form.reset()

            this.$store.commit("updateFilterParams", {})
            this.$store.commit("updateCurrentPageNumber", 1)

            try {
                await this.$store.dispatch("fetchRows")
            } catch (error) {
                return
            }
            this.showSuccess("Successfully cleared filters")
        }
    }
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
