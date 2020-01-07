<template>
    <ul id="pagination">
        <li
            :key="n"
            v-for="n in pageCount"
        >
            <a
                href="#"
                v-bind:class="{active: n === currentPageNumber}"
                v-on:click.prevent="changePage(n)"
            >{{ n }}</a>
        </li>
    </ul>
</template>

<script>
export default {
    props: {
        tableName: String
    },
    computed: {
        rowCount() {
            return this.$store.state.rowCount || 0
        },
        pageSize() {
            return this.$store.state.pageSize || 1
        },
        pageCount() {
            let count = Math.ceil(this.rowCount / this.pageSize)
            return count < 1 ? 1 : count
        },
        currentTableName() {
            return this.$store.state.currentTableName
        },
        filterParams() {
            return this.$store.state.filterParams
        },
        currentPageNumber() {
            return this.$store.state.currentPageNumber
        }
    },
    methods: {
        async changePage(pageNumber) {
            console.log("Navigating to " + pageNumber)
            this.$store.commit("updateCurrentPageNumber", pageNumber)

            await this.$store.dispatch("fetchRows")
        }
    }
}
</script>

<style scoped lang="less">
@activeColor: rgba(0, 0, 0, 0.2);

ul {
    list-style: none;
    padding: 0;

    li {
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: inline-block;
        font-size: 0.8rem;
        margin-left: 0.5rem;

        &:hover {
            background-color: @activeColor;
        }

        a {
            padding: 0.4rem 0.7rem;
            display: block;
            text-decoration: none;

            &.active {
                background-color: @activeColor;
            }
        }
    }
}
</style>
