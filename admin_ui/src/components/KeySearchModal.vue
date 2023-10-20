<template>
    <Modal
        @close="$emit('close')"
        :title="`Select a row from ${readableTableName}`"
    >
        <div class="input_wrapper">
            <font-awesome-icon icon="search" />
            <input
                autocomplete="off"
                placeholder="Type here to filter"
                type="search"
                v-model="searchTerm"
            />
        </div>

        <div class="results">
            <ul class="results_list">
                <li v-if="isFilter">
                    <a href="#" @click.prevent="selectResult(null, '')">All</a>
                </li>
                <li v-if="isNullable">
                    <a href="#" @click.prevent="selectResult(null, 'Null')"
                        >None</a
                    >
                </li>
                <li :key="id[0]" v-for="id in ids">
                    <a href="#" @click.prevent="selectResult(...id)">
                        {{ id[1] }}
                    </a>
                </li>
                <li v-if="!limitReached">
                    <a href="#" @click.prevent="loadMore"
                        ><font-awesome-icon icon="arrow-circle-down" /> Load
                        more</a
                    >
                </li>
            </ul>
        </div>
    </Modal>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

import type { FetchIdsConfig, RowID } from "../interfaces"
import Modal from "./Modal.vue"
import { titleCase } from "../utils"

const PAGE_SIZE = 5

type IDs = [RowID, string][]

export default defineComponent({
    props: {
        tableName: {
            type: String as PropType<string>,
            required: true
        },
        isFilter: {
            type: Boolean as PropType<boolean>,
            default: false
        },
        isNullable: {
            type: Boolean as PropType<boolean>,
            default: true
        }
    },
    data() {
        return {
            ids: [] as IDs,
            offset: 0,
            limitReached: false,
            searchTerm: "",
            debounceTimer: null as number | null
        }
    },
    components: {
        Modal
    },
    computed: {
        readableTableName() {
            if (!this.tableName) {
                return ""
            }

            return titleCase(this.tableName.split("_").join(" "))
        }
    },
    methods: {
        async fetchData() {
            // We fetch one more row, so we know if we've hit the limit or not.
            const config: FetchIdsConfig = {
                tableName: this.tableName,
                search: this.searchTerm,
                limit: PAGE_SIZE + 1,
                offset: this.offset
            }

            const response = await this.$store.dispatch("fetchIds", config)
            const ids: IDs = Object.entries(response.data)

            this.limitReached = ids.length <= PAGE_SIZE

            return ids.slice(0, PAGE_SIZE)
        },
        scrollResultsToBottom() {
            setTimeout(() => {
                const listElement =
                    document.getElementsByClassName("results_list")[0]
                listElement.scrollIntoView(false)
            }, 0)
        },
        async loadMore() {
            this.offset += PAGE_SIZE
            const ids = await this.fetchData()
            this.ids.push(...ids)
            this.scrollResultsToBottom()
        },
        selectResult(id: RowID | null, readable: string) {
            this.$emit("update", { id, readable })
        }
    },
    watch: {
        async tableName(value: string) {
            this.offset = 0
            if (value) {
                this.ids = await this.fetchData()
            }
        },
        async searchTerm() {
            // We debounce it, to reduce the number of API calls.
            if (this.debounceTimer) {
                clearTimeout(this.debounceTimer)
            }

            let app = this

            this.debounceTimer = window.setTimeout(async () => {
                app.offset = 0
                app.ids = await app.fetchData()
            }, 300)
        }
    },
    async mounted() {
        if (this.tableName) {
            this.ids = await this.fetchData()
        }
    }
})
</script>

<style lang="less" scoped>
@import "../vars.less";

div.input_wrapper {
    box-sizing: border-box;
    display: flex;
    align-items: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    padding: 0.5rem;

    svg {
        margin-right: 0.5rem;
    }

    input {
        display: block;
        width: 100%;
        box-sizing: border-box;
        padding: 0.5rem;
    }
}

div.results {
    max-height: 20rem;
    overflow: auto;

    ul.results_list {
        padding: 0;
        cursor: pointer;
        margin: 0;

        li {
            list-style: none;

            a {
                box-sizing: border-box;
                font-size: 0.8rem;
                padding: 0.5rem;
                display: block;
                text-decoration: none;
            }
        }
    }
}

.light_mode {
    ul.results_list {
        li:hover {
            background-color: rgba(0, 0, 0, 0.05);
        }
    }
}
.dark_mode {
    ul.results_list {
        li:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
    }
}
</style>
