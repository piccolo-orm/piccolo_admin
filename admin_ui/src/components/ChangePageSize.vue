<template>
    <div id="page_size">
        <select v-model="selectedPageSize" v-on:change="changePageSize">
            <option
                :label="`${option} per page`"
                :key="option"
                v-for="option in pageOptions"
            >
                {{ option }}
            </option>
        </select>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
            selectedPageSize: 15,
            pageOptions: [5, 15, 30, 50, 100]
        }
    },
    methods: {
        async changePageSize() {
            this.$store.commit("updatePageSize", this.selectedPageSize)
            this.$store.commit("updateCurrentPageNumber", 1)
            await this.$store.dispatch("fetchRows")
        }
    },
    computed: {
        pageSize() {
            return this.$store.state.pageSize
        }
    },
    watch: {
        pageSize() {
            this.selectedPageSize = this.pageSize
        }
    },
    mounted() {
        this.selectedPageSize = this.pageSize
    }
})
</script>

<style lang="less" scoped>
div#page_size {
    margin: 0.3rem 0 0;

    select {
        width: 7rem;
    }
}
</style>
