<template>
    <Modal @close="$emit('close')" title="Select a result">
        <div class="input_wrapper">
            <font-awesome-icon icon="search" />
            <input
                autocomplete="off"
                placeholder="Type here to filter"
                v-model="searchTerm"
            />
        </div>

        <div class="results">
            <ul class="results_list">
                <li v-if="isFilter">
                    <a href="#" @click.prevent="selectResult(null, '')">All</a>
                </li>
                <li>
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
                    <a href="#" @click.prevent="loadMore">Load more</a>
                </li>
            </ul>
        </div>
    </Modal>
</template>

<script lang="ts">
import { FetchIdsConfig } from "../interfaces"
import Modal from "./Modal.vue"

const PAGE_SIZE = 5

export default {
    props: {
        tableName: String,
        isFilter: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            ids: [],
            offset: 0,
            limitReached: false,
            searchTerm: ""
        }
    },
    components: {
        Modal
    },
    methods: {
        async fetchData() {
            // We fetch one more row, so we know if we're hit the limit or not.
            const config: FetchIdsConfig = {
                tableName: this.tableName,
                search: this.searchTerm,
                limit: PAGE_SIZE + 1,
                offset: this.offset
            }

            const response = await this.$store.dispatch("fetchIds", config)
            const ids = Object.entries(response.data)

            if (ids.length <= PAGE_SIZE) {
                this.limitReached = true
            }

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
        selectResult(id, readable) {
            this.$emit("update", { id, readable })
        }
    },
    watch: {
        async tableName() {
            this.limitReached = false
            this.offset = 0
            this.ids = await this.fetchData()
        },
        async searchTerm() {
            this.limitReached = false
            this.offset = 0
            this.ids = await this.fetchData()
        }
    },
    async mounted() {
        this.ids = await this.fetchData()
    }
}
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
            box-sizing: border-box;
            font-size: 0.8rem;
            padding: 0.5rem;
            list-style: none;

            a {
                text-decoration: none;
            }
        }
    }
}
</style>
