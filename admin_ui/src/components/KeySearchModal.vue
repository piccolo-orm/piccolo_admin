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

        <ul>
            <li v-if="isFilter" v-on:click="selectResult(null, '')">All</li>
            <li v-on:click="selectResult(null, 'Null')">None</li>
            <li :key="id[0]" v-for="id in ids" v-on:click="selectResult(...id)">
                {{ id[1] }}
            </li>
        </ul>

        <p class="extra" v-if="!limitReached">
            <a href="#" @click.prevent="loadMore">Load more</a>
        </p>
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
        async loadMore() {
            this.offset += PAGE_SIZE
            const ids = await this.fetchData()
            this.ids.push(...ids)
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

ul {
    padding: 0;
    cursor: pointer;
    margin: 0;

    li {
        box-sizing: border-box;
        color: @light_blue;
        font-size: 0.8rem;
        padding: 0.5rem;
        list-style: none;
    }
}

p.extra {
    box-sizing: border-box;
    font-size: 0.8rem;
    margin: 0;
    padding: 0.5rem;
}
</style>
