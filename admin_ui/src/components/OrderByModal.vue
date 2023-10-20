<template>
    <Modal v-on:close="$emit('close')">
        <template v-if="schema">
            <p>{{ $t("Sort by") }}:</p>

            <div v-for="(config, index) in localCopy">
                <hr v-if="index > 0" />

                <p class="remove">
                    <a
                        href="#"
                        title="Remove"
                        data-uitest="remove_column_button"
                        v-if="index > 0"
                        @click.prevent="removeOrderByColumn(index)"
                        ><font-awesome-icon icon="trash-alt"
                    /></a>
                </p>

                <select
                    name="column"
                    v-model="config.column"
                    data-uitest="sort_by_selector"
                >
                    <option :value="schema.extra.primary_key_name">
                        {{ schema.extra.primary_key_name }}
                    </option>

                    <option
                        :key="key"
                        :value="key"
                        v-for="(_, key) in schema.properties"
                    >
                        {{ key }}
                    </option>
                </select>

                <select name="ordering" v-model="config.ascending">
                    <option :value="true">{{ $t("Ascending") }}</option>
                    <option :value="false">{{ $t("Descending") }}</option>
                </select>
            </div>

            <p id="add_sort_column">
                <a
                    href="#"
                    @click.prevent="addOrderByColumn"
                    data-uitest="add_sort_column_button"
                    ><font-awesome-icon icon="plus" /> Add sort column</a
                >
            </p>

            <button @click.prevent="save" data-uitest="sort_form_button">
                {{ $t("Sort") }}
            </button>
        </template>
    </Modal>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

import Modal from "./Modal.vue"
import type { OrderByConfig, Schema } from "../interfaces"
import { syncQueryParams, getOrderByString } from "@/utils"

export default defineComponent({
    props: {
        schema: {
            type: Object as PropType<Schema>,
            required: true
        },
        tableName: {
            type: String as PropType<string>
        }
    },
    data() {
        return {
            localCopy: null as OrderByConfig[] | null
        }
    },
    components: {
        Modal
    },
    methods: {
        async save() {
            const localCopy = this.localCopy ?? []
            // Remove any which didn't specify a column to sort by.
            const orderByConfigs = localCopy.filter((i) => i.column)

            this.$store.commit("updateOrderBy", orderByConfigs)
            if (this.tableName) {
                syncQueryParams(this.tableName, {
                    __order: getOrderByString(orderByConfigs)
                })
            }

            await this.$store.dispatch("fetchRows")

            this.$emit("close")
        },
        addOrderByColumn() {
            const newValue: OrderByConfig = {
                column: null,
                ascending: true
            }
            this.localCopy?.push(newValue)
        },
        removeOrderByColumn(index: number) {
            this.localCopy?.splice(index, 1)
        }
    },
    mounted() {
        let orderByConfigs: OrderByConfig[] | null = this.$store.state.orderBy

        let localCopy: OrderByConfig[] = orderByConfigs
            ? orderByConfigs.map((i) => {
                  return { ...i }
              })
            : []

        this.localCopy = localCopy
    }
})
</script>

<style scoped lang="less">
hr {
    border: none;
}
p.remove {
    margin: 0;
    text-align: right;

    a {
        text-decoration: none;
        font-size: 0.9em;
    }
}

p#add_sort_column {
    margin: 0;

    a {
        text-decoration: none;
        font-size: 0.9em;
    }
}
</style>
