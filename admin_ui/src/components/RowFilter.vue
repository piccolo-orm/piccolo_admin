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
            <RowFormSearch
                v-bind:isFilter="true"
                v-bind:schema="schema"
            />
            <button>Apply</button>
        </form>
        <button v-on:click.prevent="clearFilters">Clear filters</button>
    </div>
</template>


<script lang="ts">
import { defineComponent } from "vue"
import RowFormSearch from "./RowFormSearch.vue"
import { APIResponseMessage } from "../interfaces"

export default defineComponent({
    props: {
        showFilterSidebar: Boolean,
    },
    components: {
        RowFormSearch,
    },
    computed: {
        schema(): any {
            return this.$store.state.schema
        },
        tableName(): string | undefined {
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

            const json = {} as any
            for (const i of form.entries()) {
                const key = i[0].split(" ").join("_")
                let value: any = i[1]

                if (value && value != "all") {
                    if (this.schema.properties[key]?.type == "array") {
                        value = JSON.parse(value).filter((i: any) => i)
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
