<template>
    <div class="key_search">
        <input
            autocomplete="off"
            :placeholder="isFilter ? 'All' : 'None'"
            type="text"
            v-model="selectedValue"
            v-on:focus="showResults = true"
            v-on:keydown.enter.prevent
        />

        <Modal
            v-show="showResults"
            @close="showResults = false"
            title="Select a result"
        >
            <div class="results">
                <div class="input_wrapper">
                    <font-awesome-icon icon="search" />
                    <input
                        autocomplete="off"
                        placeholder="Type here to filter"
                        v-model="searchTerm"
                    />
                </div>

                <ul>
                    <li
                        v-on:click="
                            selectResult(null)
                            showResults = false
                        "
                    >
                        None
                    </li>
                    <li
                        :key="id[0]"
                        v-for="id in ids"
                        v-on:click="
                            selectResult(...id)
                            showResults = false
                        "
                    >
                        {{ id[1] }}
                    </li>
                </ul>

                <p class="extra" v-if="!limitReached">
                    <a href="#" @click.prevent="loadMore">Load more</a>
                </p>
            </div>
        </Modal>

        <input
            :value="hiddenSelectedValue"
            type="hidden"
            v-bind:name="fieldName"
        />
    </div>
</template>

<script lang="ts">
import { FetchIdsConfig } from "../interfaces"
import Modal from "./Modal.vue"

const PAGE_SIZE = 15

export default {
    props: {
        fieldName: String,
        tableName: String,
        rowID: undefined,
        readable: undefined,
        isFilter: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            ids: [],
            selectedValue: undefined,
            hiddenSelectedValue: undefined,
            showResults: false,
            offset: 0,
            limitReached: false,
            searchTerm: "",
        }
    },
    components: {
        Modal,
    },
    methods: {
        async fetchData() {
            const config: FetchIdsConfig = {
                tableName: this.tableName,
                search: this.searchTerm,
                limit: PAGE_SIZE,
                offset: this.offset,
            }
            const response = await this.$store.dispatch("fetchIds", config)
            // The response is a mapping of id to readable. We convert into
            // an array of arrays like [[1, 'Bob'], ...], then sort them.
            const ids = Object.entries(response.data).sort((i, j) => {
                if (i[1] > j[1]) {
                    return 1
                }
                if (i[1] < j[1]) {
                    return -1
                }
                return 0
            })

            if (ids.length < PAGE_SIZE) {
                this.limitReached = true
            }

            this.ids.push(...ids)
        },
        async loadMore() {
            this.offset += PAGE_SIZE
            await this.fetchData()
        },
        selectResult(id, readable) {
            this.selectedValue = readable
            this.hiddenSelectedValue = id
        },
    },
    watch: {
        async tableName() {
            await this.fetchData()
        },
        async selectedValue() {
            await this.fetchData()
        },
    },
    mounted() {
        this.selectedValue = this.readable
        this.hiddenSelectedValue = this.rowID
    },
}
</script>


<style lang="less" scoped>
@import "../vars.less";

div.key_search {
    input {
        margin-bottom: 0;
    }

    div.results {
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
                // border-bottom: 1px solid rgba(0, 0, 0, 0.1);
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
    }

    margin-bottom: 0.5rem;
}

.light_mode {
    background-color: white;
    color: @dark_grey;

    .results {
        color: @dark_grey;

        li:hover {
            background-color: rgba(0, 0, 0, 0.05);
        }
    }
}

.dark_mode {
    background-color: @dark_grey;
    color: @off_white;

    .results {
        color: @off_white;

        li:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
    }
}
</style>
