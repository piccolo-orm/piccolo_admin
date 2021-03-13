<template>
    <div>
        <input
            autocomplete="off"
            placeholder="Type here to search"
            type="text"
            v-bind:name="fieldName"
            v-model="selectedValue"
            v-on:focus="
                resetResult()
                showResults = true
            "
            v-on:keydown.enter.prevent
            v-on:change="checkNull"
        />
        <div
            class="results"
            v-if="
                selectedValue != undefined &&
                showResults &&
                Object.keys(ids).length > 0
            "
        >
            <ul>
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
        </div>
        <input
            :value="hiddenSelectedValue"
            type="hidden"
            v-bind:name="fieldName"
        />
    </div>
</template>

<script lang="ts">
import { FetchIdsConfig } from "../interfaces"

export default {
    props: {
        fieldName: String,
        tableName: String,
        value: undefined,
    },
    data() {
        return {
            ids: [],
            selectedValue: undefined,
            hiddenSelectedValue: undefined,
            showResults: false,
        }
    },
    methods: {
        async fetchData() {
            const config: FetchIdsConfig = {
                tableName: this.tableName,
                search: this.selectedValue,
                limit: 15,
            }
            const response = await this.$store.dispatch("fetchIds", config)
            // The response is a mapping of id to readable. We convert into
            // an array of arrays like [[1, 'Bob'], ...], then sort them.
            this.ids = Object.entries(response.data).sort((i, j) => {
                if (i[1] > j[1]) {
                    return 1
                }
                if (i[1] < j[1]) {
                    return -1
                }
                return 0
            })
        },
        selectResult(id, readable) {
            this.selectedValue = readable
            this.hiddenSelectedValue = id
        },
        // explicit value cleaning
        resetResult() {
            this.selectedValue = undefined
            this.hiddenSelectedValue = undefined
        },
        checkNull(event) {
            // The work around for setting a value of Null, is to type it in.
            if (event.target.value.toUpperCase() == "NULL") {
                console.log("Setting as null")
                this.hiddenSelectedValue = null
            }
        },
    },
    watch: {
        async tableName() {
            await this.fetchData()
        },
        async selectedValue(searchValue) {
            await this.fetchData()
        },
    },
    mounted() {
        this.selectedValue = this.value
        this.hiddenSelectedValue = this.value
    },
}
</script>


<style lang="less" scoped>
@import "../vars.less";

.results {
    box-sizing: border-box;
    padding: 0.5rem;
    cursor: pointer;

    ul {
        margin: 0;
        padding: 0;

        li {
            box-sizing: border-box;
            padding: 0.2rem;
            list-style: none;
        }
    }
}

.light_mode {
    background-color: white;
    color: @dark_grey;

    .results {
        background-color: darken(white, 5%);
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
        background-color: darken(@dark_grey, 4%);
        color: @off_white;

        li:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
    }
}
</style>
