<template>
    <p>
        Show
        <select
            id="page_size"
            v-model="selectedPageSize"
            v-on:click.prevent="$emit('triggered')"
        >
            <option
                v-bind:key="option"
                v-for="option in pageOptions"
            >{{ option }}</option>
            {{ pageSize }}
        </select>
        results
    </p>
</template>

<script>
export default {
    data() {
        return {
            selectedPageSize: 5,
            pageOptions: [5, 10, 25, 50, 100],
        }
    },
    computed: {
        pageSize() {
            this.$store.state.pageSize = this.selectedPageSize
            return this.$store.state.pageSize
        },
    },
}
</script>

<style lang="less" scoped>
select#page_size {
    width: 3.3rem;
    margin-bottom: -5px;
}
</style>