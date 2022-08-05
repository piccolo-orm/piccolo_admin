<template>
    <div>
        <ul class="array_items">
            <li :key="index" v-for="(value, index) in internalArray">
                <input
                    :type="inputType"
                    :value="value"
                    id="choice"
                    v-on:change="updateArray($event, index)"
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
                >
                    <font-awesome-icon icon="plus" title="Add" />{{ $t("Add") }}
                </a>
            </li>
        </ul>
        <MediaViewer
            v-if="showMediaViewer"
            :mediaViewerConfig="mediaViewerConfig"
            @close="showMediaViewer = false"
        />
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue"
import MediaViewer from "./MediaViewer.vue"
import { MediaViewerConfig } from "@/interfaces"

export default Vue.extend({
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
        }
    },
    components: {
        MediaViewer
    },
    data() {
        return {
            internalArray: [],
            showMediaViewer: false,
            mediaViewerConfig: null as MediaViewerConfig
        }
    },
    computed: {
        schema() {
            return this.$store.state.schema
        },
        currentTableName() {
            return this.$store.state.currentTableName
        },
        isMediaColumn() {
            return this.schema.media_columns.includes(this.fieldName)
        }
    },
    methods: {
        updateArray($event, index: number) {
            this.$set(this.internalArray, index, $event.target.value)
            this.$emit("updateArray", this.internalArray)
        },
        addArrayElement() {
            this.internalArray = [...this.internalArray, ""]
            this.$emit("updateArray", this.internalArray)
        },
        removeArrayElement(index: number) {
            this.$delete(this.internalArray, index)
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
        array() {
            this.internalArray = [...this.array]
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

        input {
            flex-grow: 1;
            margin-right: 0.5rem;
            margin-bottom: 0 !important;
        }
    }
}
</style>
