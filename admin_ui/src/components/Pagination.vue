<template>
    <div id="pagination">
        <ul
            class="pages"
            v-if="pageCount < 20"
        >
            <li
                :key="n"
                v-for="n in pageCount"
            >
                <a
                    class="subtle"
                    href="#"
                    v-bind:class="{active: n === currentPageNumber}"
                    v-on:click.prevent="changePage(n)"
                >{{ n }}</a>
            </li>
        </ul>

        <div
            class="page_select"
            v-else
        >
            <label>Go to page</label>
            <select v-model="pageDropdownValue">
                <option
                    :key="n"
                    v-for="n in pageCount"
                >{{ n }}</option>
            </select>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        tableName: String,
    },
    data() {
        return {
            pageDropdownValue: 0,
        }
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
        },
    },
    methods: {
        async changePage(pageNumber) {
            console.log("Navigating to " + pageNumber)
            this.$store.commit("updateCurrentPageNumber", pageNumber)

            await this.$store.dispatch("fetchRows")
        },
    },
    watch: {
        pageDropdownValue(value) {
            this.changePage(value)
        },
    },
    mounted() {
        this.pageDropdownValue = this.currentPageNumber
    },
}
</script>

<style scoped lang="less">
@activeColor: rgba(0, 0, 0, 0.2);

div#pagination {
    ul.pages {
        list-style: none;
        padding: 0;

        li {
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: inline-block;
            font-size: 0.8rem;
            margin-left: 0.5rem;
            margin-top: 0.5rem;

            a {
                padding: 0.4rem 0.7rem;
                display: block;
                text-decoration: none;

                &:hover {
                    background-color: @activeColor;
                }

                &.active {
                    background-color: @activeColor;
                }
            }
        }
    }

    div.page_select {
        select,
        label {
            display: inline-block;
        }

        label {
            margin-right: 1rem;
        }

        select {
            width: auto;
        }
    }
}
</style>
