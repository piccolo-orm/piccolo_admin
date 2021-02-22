<template>
    <div>
        <input
            :placeholder="'Search ' + tableName + 's'"
            autocomplete="off"
            type="text"
            v-bind:name="fieldName"
            v-model="selectedValue"
            v-on:focus="resetResult(), toggle = true"
            v-on:keydown.enter.prevent
        />
        <div
            id="results"
            v-if="toggle"
        >
            <div
                :key="id"
                v-for="(readable, id) in dropdownItems"
                v-on:click="selectResult(readable, id), toggle = false"
                v-on:focus="resetResult(), toggle = true"
            >{{ readable }}</div>
        </div>
        <input
            :value="hiddenSelectedValue"
            type="hidden"
            v-bind:name="fieldName"
            v-on:focus="toggle = true"
        />
    </div>
</template>

<script>
export default {
    props: {
        fieldName: String,
        tableName: String,
        value: undefined,
    },
    data() {
        return {
            ids: [],
            dropdownItems: {},
            selectedValue: undefined,
            hiddenSelectedValue: undefined,
            toggle: false,
        }
    },
    methods: {
        async fetchData() {
            const response = await this.$store.dispatch(
                "fetchIds",
                this.tableName
            )
            this.ids = response.data
        },
        selectResult(readable, id) {
            this.selectedValue = readable
            this.hiddenSelectedValue = id
        },
        // need to explicit clear values
        resetResult() {
            this.selectedValue = undefined
            this.hiddenSelectedValue = undefined
        },
    },
    watch: {
        async tableName() {
            await this.fetchData()
        },
        selectedValue(searchValue) {
            this.dropdownItems = {}
            for (const property in this.ids) {
                if (
                    this.ids[property]
                        .toLowerCase()
                        .includes(searchValue.toLowerCase())
                ) {
                    this.dropdownItems[property] = this.ids[property]
                }
            }
        },
    },
    async mounted() {
        this.selectedValue = this.value
        this.hiddenSelectedValue = this.value
        await this.fetchData()
    },
}
</script>


<style lang="less" scoped>
@import "../vars.less";

.light_mode {
    background-color: white;
    color: @dark_grey;
    #results {
        cursor: pointer;
        background-color: darken(white, 5%);
        color: @dark_grey;
    }
}

.dark_mode {
    background-color: @dark_grey;
    color: @off_white;
    #results {
        cursor: pointer;
        background-color: darken(@dark_grey, 4%);
        color: @off_white;
    }
}
</style>