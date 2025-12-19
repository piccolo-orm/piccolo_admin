<template>
    <div id="pagination">
        <ul class="pages">
            <!-- Previous pages -->
            <li v-for="n in prevPages" :key="n">
                <a class="subtle" href="#" v-on:click.prevent="changePage(n)">
                    <font-awesome-icon icon="angle-left" />
                </a>
            </li>

            <!-- Current page input -->
            <li class="current">
                <input
                    type="number"
                    :min="1"
                    :max="pageCount"
                    v-model.number="pageInput"
                    v-on:keyup.enter="goToPage"
                />
            </li>
            <li class="count">of {{ pageCount }}</li>

            <!-- Next pages -->
            <li v-for="n in nextPages" :key="n">
                <a href="#" class="subtle" v-on:click.prevent="changePage(n)">
                    <font-awesome-icon icon="angle-right" />
                </a>
            </li>
        </ul>
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
            pageInput: 1
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
            const count = Math.ceil(this.rowCount / this.pageSize)
            return count < 1 ? 1 : count
        },
        currentPageNumber() {
            return this.$store.state.currentPageNumber || 1
        },

        prevPages(): number[] {
            const start = Math.max(1, this.currentPageNumber - 1)
            const end = this.currentPageNumber - 1
            return this.range(start, end)
        },

        nextPages(): number[] {
            const start = this.currentPageNumber + 1
            const end = Math.min(this.pageCount, this.currentPageNumber + 1)
            return this.range(start, end)
        }
    },
    methods: {
        range(start: number, end: number): number[] {
            if (start > end) return []
            // return rows for correct page
            return Array.from({ length: end - start + 1 }, (_, i) => start + i)
        },

        async changePage(page: number) {
            // return first or last page
            if (page < 1 || page > this.pageCount) return
            // return current page
            if (page === this.currentPageNumber) return

            this.$store.commit("updateCurrentPageNumber", page)
            await this.$store.dispatch("fetchRows")
        },

        async goToPage() {
            let page = this.pageInput

            if (!page || page < 1) page = 1
            if (page > this.pageCount) page = this.pageCount

            this.pageInput = page
            await this.changePage(page)
        }
    },
    watch: {
        currentPageNumber(value: number) {
            this.pageInput = value
        }
    },
    mounted() {
        this.pageInput = this.currentPageNumber
    }
})
</script>

<style scoped lang="less">
@activeColor: rgba(0, 0, 0, 0.2);

div#pagination {
    ul.pages {
        list-style: none;
        margin: 0.3rem 0;
        padding: 0;

        li {
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
    span.count {
        padding-right: 0.5rem;
    }
}

@media (max-width: 480px) {
    div#pagination {
        ul.pages {
            li {
                font-size: 0.6rem;
            }
        }
    }
}
</style>
