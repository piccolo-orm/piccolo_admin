<template>
    <div v-if="row">
        <div
            v-bind:key="columnName"
            v-for="(property, columnName) in schema.properties"
        >
            <label>
                {{ property.title }}
                <span class="required" v-if="isRequired(String(columnName))"
                    >*</span
                >
                <Tooltip
                    v-if="property.extra.help_text"
                    :content="property.extra.help_text"
                />

                <template v-if="property.extra.foreign_key">
                    <router-link
                        :to="{
                            name: 'addRow',
                            params: { tableName: property.extra.foreign_key.to }
                        }"
                        class="add"
                        target="_blank"
                        v-if="!isFilter"
                    >
                        <font-awesome-icon icon="plus" />
                    </router-link>

                    <router-link
                        v-if="!isFilter && foreignKeyIDs[columnName]"
                        :to="{
                            name: 'editRow',
                            params: {
                                tableName: property.extra.foreign_key.to,
                                rowID: foreignKeyIDs[columnName]
                            }
                        }"
                        class="add"
                        target="_blank"
                    >
                        <font-awesome-icon icon="edit" />
                    </router-link>
                </template>
            </label>

            <KeySearch
                v-if="property.extra.foreign_key"
                v-bind:fieldName="String(columnName)"
                v-bind:tableName="property.extra.foreign_key.to"
                v-bind:rowID="getValue(String(columnName))"
                v-bind:readable="getValue(columnName + '_readable')"
                v-bind:isNullable="property.extra.nullable"
                @update="foreignKeyIDs[String(columnName)] = $event.id"
            />
            <InputField
                v-else
                v-bind:columnName="String(columnName)"
                v-bind:format="getFormat(property)"
                v-bind:isFilter="isFilter"
                v-bind:isNullable="property.extra.nullable"
                v-bind:required="isRequired(String(columnName))"
                v-bind:type="getType(property)"
                v-bind:value="getValue(String(columnName))"
                v-bind:choices="property.extra.choices"
                v-bind:isMediaColumn="isMediaColumn(String(columnName))"
                v-bind:isRichText="isRichText(String(columnName))"
                v-bind:widget="property.extra.widget"
                v-bind:timeResolution="
                    schema?.extra?.time_resolution[columnName]
                "
            />
        </div>
    </div>
</template>

<script lang="ts">
import { computed, defineComponent, type PropType, reactive, toRefs } from "vue"

import KeySearch from "./KeySearch.vue"
import InputField from "./InputField.vue"
import Tooltip from "./Tooltip.vue"
import { type Schema, getFormat, getType } from "@/interfaces"

export default defineComponent({
    props: {
        row: {
            type: Object,
            required: true
        },
        schema: {
            type: Object as PropType<Schema>,
            required: true
        },
        isFilter: {
            type: Boolean as PropType<boolean>,
            default: false
        }
    },
    components: {
        InputField,
        KeySearch,
        Tooltip
    },
    setup(props) {
        const { schema, row } = toRefs(props)

        const foreignKeyColumnNames = computed(() => {
            const _foreignKeyColumnNames: string[] = []

            Object.entries(schema.value.properties).forEach((value) => {
                const [columnName, property] = value
                if (property.extra.foreign_key) {
                    _foreignKeyColumnNames.push(columnName)
                }
            })

            return _foreignKeyColumnNames
        })

        const foreignKeyIDs = computed(() => {
            const _foreignKeyIDs: { [key: string]: any } = {}
            foreignKeyColumnNames.value.forEach((columnName) => {
                _foreignKeyIDs[columnName] = row.value[columnName]
            })

            return reactive(_foreignKeyIDs)
        })

        return {
            foreignKeyIDs,
            getFormat,
            getType
        }
    },
    methods: {
        getValue(columnName: string) {
            let value = this.row ? this.row[columnName] : undefined
            return value
        },
        isRequired(columnName: string) {
            return (
                !this.isFilter &&
                (this.schema.required || []).indexOf(columnName) != -1
            )
        },
        isMediaColumn(columnName: string) {
            return this.schema.extra.media_columns.includes(columnName)
        },
        isRichText(columnName: string) {
            return this.schema.extra.rich_text_columns.includes(columnName)
        }
    }
})
</script>

<style scoped lang="less">
.add {
    float: right;
}

span.required {
    opacity: 0.5;
    padding-left: 0.05rem;
}
</style>
