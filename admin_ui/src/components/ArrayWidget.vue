<template>
    <div :data-uitest="`${fieldName}_array_widget`">
        <ul class="array_items">
            <li :key="value" v-for="(value, index) in internalArray">
                <!--
                We deliberately set the `fieldName` to blank, as we don't
                want the value to be submitted. Instead, we combine the
                values into an array object and submit that instead.

                Also, `isFilter` is deliberately always `false`. We don't want
                the 'All' option to be shown. For arrays, 'All' is the absence
                of any values.
                -->
                <ChoiceSelect
                    v-if="choices"
                    :fieldName="''"
                    :value="value"
                    :choices="choices"
                    :isNullable="isNullable"
                    :isFilter="false"
                    :isArray="true"
                    @updated="updateArray($event, index)"
                />
                <input
                    v-else
                    :type="inputType"
                    :value="value"
                    @change="updateArray(getValueFromEvent($event), index)"
                />

                <a
                    href="#"
                    v-on:click.prevent="showMedia(index)"
                    :value="value"
                    v-if="isMediaColumn && !isFilter"
                    ><font-awesome-icon icon="eye" title="View"
                /></a>
                <a href="#" v-on:click.prevent="removeArrayElement(index)">
                    <font-awesome-icon icon="times" title="Remove" />
                </a>
            </li>
            <li>
                <a
                    class="add"
                    href="#"
                    v-on:click.prevent="addArrayElement"
                    v-if="enableAddButton"
                    data-uitest="add_array_item_button"
                >
                    <font-awesome-icon icon="plus" title="Add" />{{ $t("Add") }}
                </a>
            </li>
        </ul>
        <MediaViewer
            v-if="showMediaViewer && mediaViewerConfig"
            :mediaViewerConfig="mediaViewerConfig"
            @close="showMediaViewer = false"
        />
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

import ChoiceSelect from "./ChoiceSelect.vue"
import MediaViewer from "./MediaViewer.vue"
import type { Choices, MediaViewerConfig, Schema } from "@/interfaces"

export default defineComponent({
    props: {
        array: {
            type: Array as PropType<string[]>,
            default: () => []
        },
        inputType: {
            type: String as PropType<string>,
            default: "text"
        },
        fieldName: {
            type: String as PropType<string>,
            default: ""
        },
        enableAddButton: {
            type: Boolean as PropType<boolean>,
            default: true
        },
        isFilter: {
            type: Boolean as PropType<boolean>,
            default: true
        },
        choices: {
            type: Object as PropType<Choices | null>,
            default: null
        },
        isNullable: {
            type: Boolean as PropType<boolean>,
            default: false
        }
    },
    components: {
        ChoiceSelect,
        MediaViewer
    },
    data() {
        return {
            internalArray: [] as any[],
            showMediaViewer: false,
            mediaViewerConfig: null as MediaViewerConfig | null
        }
    },
    computed: {
        schema(): Schema {
            return this.$store.state.schema
        },
        currentTableName() {
            return this.$store.state.currentTableName
        },
        isMediaColumn() {
            return this.schema?.extra.media_columns.includes(this.fieldName)
        }
    },
    methods: {
        getValueFromEvent(event: Event) {
            return (event.target as HTMLInputElement).value
        },
        updateArray(value: any, index: number) {
            this.internalArray[index] = value
            this.$emit("updateArray", this.internalArray)
        },
        addArrayElement() {
            this.internalArray = [...this.internalArray, ""]
            this.$emit("updateArray", this.internalArray)
        },
        removeArrayElement(index: number) {
            this.internalArray.splice(index, 1)
            this.$emit("updateArray", this.internalArray)
        },
        showMedia(index: number) {
            const mediaViewerConfig: MediaViewerConfig = {
                fileKey: this.internalArray[index],
                columnName: this.fieldName,
                tableName: this.currentTableName
            }
            this.mediaViewerConfig = mediaViewerConfig
            this.showMediaViewer = true
        }
    },
    watch: {
        array(newValue) {
            this.internalArray = newValue ? [...newValue] : []
        }
    },
    mounted() {
        this.internalArray = [...this.array]
    }
})
</script>

<style scoped lang="less">
ul.array_items {
    padding: 0;
    width: 100%;

    li {
        display: flex;
        flex-direction: row;
        list-style: none;
        margin-bottom: 0.8rem;
        align-items: center;

        a {
            text-decoration: none;

            &.add {
                font-size: 0.9em;
            }
        }

        input,
        select {
            flex-grow: 1;
            margin-right: 0.5rem;
            margin-bottom: 0 !important;
        }
    }
}
</style>
