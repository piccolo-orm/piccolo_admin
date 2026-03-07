<template>
    <div id="pagination">
        <ul class="pages">
            <li>
                <a
                    class="subtle"
                    href="#"
                    v-on:click.prevent="changePage(currentPageNumber - 1)"
                    :class="{ disabled: currentPageNumber == 1 }"
                >
                    <font-awesome-icon icon="angle-left" />
                </a>
            </li>

            <li class="current">
                <input
                    type="number"
                    :min="1"
                    :max="pageCount"
                    v-model.number="pageInput"
                    v-on:keyup.enter="
                        changePage(
                            Number(($event.target as HTMLInputElement).value)
                        )
                    "
                    v-on:change="
                        changePage(
                            Number(($event.target as HTMLInputElement).value)
                        )
                    "
                />
            </li>
            <li class="count">of {{ pageCount }}</li>

            <li>
                <a
                    href="#"
                    class="subtle"
                    v-on:click.prevent="changePage(currentPageNumber + 1)"
                    :class="{ disabled: currentPageNumber == pageCount }"
                >
                    <font-awesome-icon icon="angle-right" />
                </a>
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
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
            return this.$store.state.currentPageNumber
        }
    },
    methods: {
        async changePage(page: number) {
            if (page < 1) {
                this.pageInput = 1
                return
            }

            if (page > this.pageCount) {
                this.pageInput = this.pageCount
                return
            }

            if (page === this.currentPageNumber) {
                return
            }

            this.$store.commit("updateCurrentPageNumber", page)
            await this.$store.dispatch("fetchRows")
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

                &.disabled {
                    color: grey;
                    cursor: initial;

                    &:hover {
                        background: none;
                    }
                }
            }
        }
    }
    span.count {
        padding-right: 0.5rem;
    }
    input {
        text-align: center;
    }
}
</style>
