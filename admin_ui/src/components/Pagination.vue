<template>
    <div id="pagination">
        <ul class="pages" v-if="pageCount < 20">
            <li :key="n" v-for="n in pageCount">
                <a
                    class="subtle"
                    href="#"
                    v-bind:class="{ active: n === currentPageNumber }"
                    v-on:click.prevent="changePage(n)"
                    >{{ n }}</a
                >
            </li>
        </ul>

        <div class="page_select" v-else>
            <label>{{ $t("Go to page") }}</label>
            <select v-model="pageDropdownValue">
                <option :key="n" v-for="n in pageCount">{{ n }}</option>
            </select>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
    props: {
        tableName: String
    },
    data() {
        return {
            pageDropdownValue: 0
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
        }
    },
    methods: {
        async changePage(pageNumber: number) {
            if (this.currentPageNumber != pageNumber) {
                console.log("Navigating to " + pageNumber)
                this.$store.commit("updateCurrentPageNumber", pageNumber)
                await this.$store.dispatch("fetchRows")
            }
        }
    },
    watch: {
        pageDropdownValue(value) {
            this.changePage(value)
        }
    },
    mounted() {
        this.pageDropdownValue = this.currentPageNumber
    }
})
</script>

<style scoped lang="less">
@activeColor: rgba(0, 0, 0, 0.2);

div#pagination {
    ul.pages {
        list-style: none;
        margin: 0.5rem 0;
        padding: 0;

        li {
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: inline-block;
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
            margin-right: 0.5rem;

            &:last-child {
                margin-right: 0;
            }

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
            font-size: 0.9rem;
            margin-right: 1rem;
        }

        select {
            width: auto;
            padding-right: 1.5rem;
        }
    }
}
</style>
