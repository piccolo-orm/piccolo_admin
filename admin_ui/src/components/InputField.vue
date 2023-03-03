<template>
    <div>
        <template v-if="isMediaColumn && !isFilter">
            <div class="media_block">
                <input type="file" @change="uploadFile($event)" />
                <a
                    href="#"
                    @click.prevent="showMedia"
                    v-if="localValue && type != 'array'"
                    ><font-awesome-icon icon="eye" title="View"
                /></a>
            </div>

            <MediaViewer
                v-if="showMediaViewer"
                :mediaViewerConfig="mediaViewerConfig"
                @close="showMediaViewer = false"
            />

            <LoadingOverlay v-if="showLoadingOverlay" />
        </template>

        <template v-if="choices && type != 'array'">
            <OperatorField :columnName="columnName" v-if="isFilter" />
            <ChoiceSelect
                :choices="choices"
                :fieldName="columnName"
                :isFilter="isFilter"
                :isNullable="isNullable"
                :value="value"
            />
        </template>

        <template v-else-if="type == 'integer'">
            <OperatorField :columnName="columnName" v-if="isFilter" />
            <input
                step="1"
                type="number"
                v-bind:name="columnName"
                v-bind:placeholder="placeholder"
                v-bind:value="value"
            />
        </template>

        <template v-else-if="type == 'string'">
            <template
                v-if="['date-time', 'date', 'time'].indexOf(format) != -1"
            >
                <OperatorField :columnName="columnName" v-if="isFilter" />
                <!--
                `disableMobile` is very poorly named - setting it to 'true'
                enables the picker on mobile devices. It doesn't work great on
                iOS, so an alternative picker is needed.
                -->
                <flat-pickr
                    v-bind:config="{
                        enableTime: ['date-time', 'time'].indexOf(format) != -1,
                        disableMobile: true,
                        noCalendar: format == 'time'
                    }"
                    v-bind:name="columnName"
                    v-model="localValue"
                ></flat-pickr>
            </template>

            <div v-else-if="format == 'text-area' && isFilter == false">
                <vue-editor
                    v-if="isRichText"
                    v-model="localValue"
                    v-bind:name="columnName"
                    :editor-toolbar="customToolbar"
                />
                <textarea
                    v-else
                    autocomplete="off"
                    ref="textarea"
                    v-bind:name="columnName"
                    v-bind:placeholder="placeholder"
                    v-bind:style="{ height: textareaHeight }"
                    v-model="localValue"
                    v-on:input="setTextareaHeight"
                />

                <textarea
                    id="editor"
                    v-model.lazy="localValue"
                    v-bind:name="columnName"
                ></textarea>
            </div>

            <div v-else-if="format == 'json'">
                <textarea
                    :value="
                        localValue
                            ? JSON.stringify(JSON.parse(localValue), null, 2)
                            : null
                    "
                    autocomplete="off"
                    ref="textarea"
                    v-bind:name="columnName"
                    v-bind:style="{ height: textareaHeight }"
                    v-on:input="setTextareaHeight"
                />
            </div>

            <input
                type="text"
                v-bind:name="columnName"
                v-bind:placeholder="placeholder"
                v-else
                v-model="localValue"
            />
        </template>

        <template v-else-if="type == 'boolean'">
            <select v-bind:name="columnName">
                <option
                    v-bind:selected="value == 'all'"
                    v-if="isFilter"
                    value="all"
                >
                    All
                </option>
                <option
                    v-bind:selected="value == null"
                    v-if="isNullable"
                    value="null"
                >
                    Null
                </option>
                <option v-bind:selected="value == true" value="true">
                    True
                </option>
                <option v-bind:selected="value == false" value="false">
                    False
                </option>
            </select>
        </template>

        <template v-else-if="type == 'number'">
            <template v-if="format == 'time-delta'">
                <OperatorField :columnName="columnName" v-if="isFilter" />
                <DurationWidget
                    v-bind:timedelta="localValue"
                    v-on:newTimedelta="updateLocalValue($event)"
                />
                <input
                    type="hidden"
                    v-bind:name="columnName"
                    v-model="localValue"
                />
            </template>
            <template v-else>
                <OperatorField :columnName="columnName" v-if="isFilter" />
                <input
                    type="text"
                    v-bind:name="columnName"
                    v-bind:placeholder="placeholder"
                    v-model="localValue"
                />
            </template>
        </template>

        <template v-else-if="type == 'array'">
            <ArrayWidget
                :array="localValue"
                :enableAddButton="isFilter || !isMediaColumn"
                v-on:updateArray="localValue = $event"
                :fieldName="columnName"
                :isFilter="isFilter"
                :choices="choices"
                :isNullable="isNullable"
            />
            <input
                :value="localValue ? JSON.stringify(localValue) : null"
                type="hidden"
                v-bind:name="columnName"
            />
        </template>
    </div>
</template>

<script lang="ts">
import Vue, { PropType } from "vue"
import axios from "axios"
import flatPickr from "vue-flatpickr-component"
import { VueEditor } from "vue2-editor"

import ArrayWidget from "./ArrayWidget.vue"
import ChoiceSelect from "./ChoiceSelect.vue"
import DurationWidget from "./DurationWidget.vue"
import LoadingOverlay from "./LoadingOverlay.vue"
import MediaViewer from "./MediaViewer.vue"
import OperatorField from "./OperatorField.vue"
import {
    Choices,
    StoreFileAPIResponse,
    APIResponseMessage,
    MediaViewerConfig
} from "@/interfaces"

export default Vue.extend({
    props: {
        // A nicely formatted column name, for example 'First Name'
        title: {
            type: String as PropType<string>,
            required: true
        },
        columnName: {
            type: String as PropType<string>,
            required: true
        },
        type: {
            type: String as PropType<string>,
            default: "string"
        },
        value: {
            type: undefined as PropType<any>,
            default: undefined
        },
        // Fields can share the same type, but have different formats. For
        // example, 'text-area', when type is 'string'.
        format: {
            type: String as PropType<string | undefined>,
            default: undefined
        },
        isFilter: {
            type: Boolean as PropType<boolean>,
            default: true
        },
        isNullable: {
            type: Boolean as PropType<boolean>,
            default: false
        },
        choices: {
            type: Object as PropType<Choices>,
            default: null
        },
        isMediaColumn: {
            type: Boolean as PropType<boolean>,
            default: false
        },
        isRichText: {
            type: Boolean as PropType<boolean>,
            default: false
        }
    },
    components: {
        flatPickr,
        ArrayWidget,
        ChoiceSelect,
        DurationWidget,
        LoadingOverlay,
        MediaViewer,
        OperatorField,
        VueEditor
    },
    data() {
        return {
            localValue: undefined,
            textareaHeight: "50px",
            showMediaViewer: false,
            mediaViewerConfig: null as MediaViewerConfig,
            customToolbar: [
                ["bold", "italic", "underline", "strike", "blockquote"],
                [{ list: "ordered" }, { list: "bullet" }],
                [{ indent: "-1" }, { indent: "+1" }],
                [
                    { align: "" },
                    { align: "center" },
                    { align: "right" },
                    { align: "justify" }
                ],
                ["link", "image", "code-block"],
                [{ header: [false, 1, 2, 3] }]
            ],
            showLoadingOverlay: false
        }
    },
    computed: {
        placeholder() {
            if (this.isFilter) {
                return "All"
            } else if (this.isNullable && this.value === null) {
                return "NULL"
            } else {
                return ""
            }
        },
        currentTableName() {
            return this.$store.state.currentTableName
        }
    },
    methods: {
        setTextareaHeight() {
            let element = this.$refs.textarea
            if (element) {
                if (element.scrollHeight > element.clientHeight) {
                    this.textareaHeight = element.scrollHeight + "px"
                }
            }
        },
        updateLocalValue(event) {
            this.localValue = event
        },
        showMedia() {
            const mediaViewerConfig: MediaViewerConfig = {
                fileKey: this.localValue,
                columnName: this.columnName,
                tableName: this.currentTableName
            }
            this.mediaViewerConfig = mediaViewerConfig
            this.showMediaViewer = true
        },
        async uploadFile(event) {
            const file = event.target.files[0]

            if (!file) {
                return
            }

            let formData = new FormData()
            formData.append("table_name", this.currentTableName)
            formData.append("column_name", this.columnName)
            formData.append("file", file)

            this.showLoadingOverlay = true

            try {
                const response = await axios.post<StoreFileAPIResponse>(
                    "./api/media/",
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data"
                        }
                    }
                )
                if (this.type == "array") {
                    if (this.localValue) {
                        this.localValue.push(response.data.file_key)
                    } else {
                        this.localValue = [response.data.file_key]
                    }
                } else {
                    this.localValue = response.data.file_key
                }
            } catch (error) {
                let errorMessage = "The request failed."
                const statusCode = error.response?.status

                if (statusCode) {
                    if (statusCode == 413) {
                        errorMessage = "The file is too large."
                    } else if (statusCode == 500) {
                        errorMessage = "An error happened on the server."
                    } else {
                        errorMessage =
                            error.response?.data?.detail ?? "Unknown error"
                    }
                }

                let message: APIResponseMessage = {
                    contents: errorMessage,
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)
            }

            event.target.value = ""
            this.showLoadingOverlay = false
        }
    },
    watch: {
        value() {
            this.localValue = this.value
            this.setTextareaHeight()
        },
        currentTableName() {
            this.localValue = undefined
        }
    },
    mounted() {
        this.localValue = this.value

        let app = this
        setTimeout(function () {
            app.setTextareaHeight()
        }, 0)
    }
})
</script>

<style scoped lang="less">
@import "../vars.less";

pre {
    white-space: pre-wrap;
    word-break: break-all;
}

input.flatpicker-input {
    box-sizing: border-box;
    padding: 0.5rem;
    width: 100%;
}

input[type="file"] {
    margin-bottom: 0.5rem;
}

textarea#editor {
    display: none;
}

div.media_block {
    display: flex;
    flex-direction: row;

    input {
        flex-grow: 1;
    }

    a {
        text-align: right;
        flex-shrink: 0;
        text-decoration: none;
    }
}
</style>
