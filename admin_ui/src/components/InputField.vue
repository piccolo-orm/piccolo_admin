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
                v-if="showMediaViewer && mediaViewerConfig"
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
                v-if="
                    format &&
                    ['date-time', 'date', 'time'].indexOf(format) != -1
                "
            >
                <OperatorField :columnName="columnName" v-if="isFilter" />

                <input
                    v-if="format == 'date'"
                    type="date"
                    v-bind:name="columnName"
                    v-bind:placeholder="placeholder"
                    v-model="localValue"
                />

                <template v-if="format == 'time'">
                    <TimeWidget
                        :time="localValue"
                        :placeholder="placeholder"
                        :timeResolution="timeResolution ?? 1"
                        @update="localValue = $event"
                    />
                    <input
                        type="hidden"
                        v-bind:name="columnName"
                        v-model="localValue"
                    />
                </template>

                <template v-if="format == 'date-time'">
                    <template v-if="widget == 'timestamptz'">
                        <TimestamptzWidget
                            :datetime="localValue"
                            :placeholder="placeholder"
                            :timeResolution="timeResolution ?? 1"
                            @update="localValue = $event"
                        />
                        <input
                            type="hidden"
                            v-bind:name="columnName"
                            v-model="localValue"
                        />
                    </template>
                    <template v-else>
                        <TimestampWidget
                            :datetime="localValue"
                            :placeholder="placeholder"
                            :timeResolution="timeResolution ?? 1"
                            @update="localValue = $event"
                        />
                        <input
                            type="hidden"
                            v-bind:name="columnName"
                            v-model="localValue"
                        />
                    </template>
                </template>
            </template>

            <div v-else-if="widget == 'text-area' && isFilter == false">
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
                    v-on:keyup="setTextareaHeight"
                />

                <textarea
                    id="editor"
                    v-model.lazy="localValue"
                    v-bind:name="columnName"
                ></textarea>
            </div>

            <div v-else-if="format == 'duration'">
                <OperatorField :columnName="columnName" v-if="isFilter" />
                <DurationWidget
                    v-bind:timedelta="convertDurationToSeconds"
                    v-on:newTimedelta="localValue = $event"
                />
                <input
                    type="hidden"
                    v-bind:name="columnName"
                    :value="convertSecondsToDuration"
                />
            </div>

            <div v-else-if="widget == 'json'">
                <textarea
                    v-model="localValue"
                    autocomplete="off"
                    ref="textarea"
                    v-bind:name="columnName"
                    v-bind:style="{ height: textareaHeight }"
                    v-bind:placeholder="placeholder"
                    v-on:keyup="setTextareaHeight"
                />
            </div>

            <template v-else>
                <MatchField v-if="isFilter" :columnName="columnName" />

                <input
                    type="text"
                    v-bind:name="columnName"
                    v-bind:placeholder="placeholder"
                    v-model="localValue"
                />
            </template>
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
            <OperatorField :columnName="columnName" v-if="isFilter" />
            <input
                type="text"
                v-bind:name="columnName"
                v-bind:placeholder="placeholder"
                v-model="localValue"
            />
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
                :inputType="arrayInputType"
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
import { defineComponent, type PropType } from "vue"
import axios from "axios"
import moment from "moment"
// @ts-ignore
import { VueEditor } from "vue3-editor"

import ArrayWidget from "./ArrayWidget.vue"
import ChoiceSelect from "./ChoiceSelect.vue"
import DurationWidget from "./DurationWidget.vue"
import LoadingOverlay from "./LoadingOverlay.vue"
import MatchField from "./MatchField.vue"
import MediaViewer from "./MediaViewer.vue"
import OperatorField from "./OperatorField.vue"
import TimeWidget from "./TimeWidget.vue"
import TimestampWidget from "./TimestampWidget.vue"
import TimestamptzWidget from "./TimestamptzWidget.vue"
import type {
    Choices,
    StoreFileAPIResponse,
    APIResponseMessage,
    MediaViewerConfig
} from "@/interfaces"
import { secondsToISO8601Duration } from "../utils"

export default defineComponent({
    props: {
        columnName: {
            type: String as PropType<string>,
            required: true
        },
        type: {
            type: String as PropType<string>,
            default: "string"
        },
        value: {
            type: undefined as PropType<any> | undefined,
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
            type: Object as PropType<Choices | null>,
            default: null
        },
        isMediaColumn: {
            type: Boolean as PropType<boolean>,
            default: false
        },
        isRichText: {
            type: Boolean as PropType<boolean>,
            default: false
        },
        // The API can indicate which widget is desired.
        widget: {
            type: undefined as unknown as PropType<string | undefined>,
            default: undefined
        },
        timeResolution: {
            type: undefined as unknown as PropType<number | undefined>,
            default: undefined
        }
    },
    components: {
        ArrayWidget,
        ChoiceSelect,
        DurationWidget,
        LoadingOverlay,
        MatchField,
        MediaViewer,
        OperatorField,
        TimestampWidget,
        TimestamptzWidget,
        TimeWidget,
        VueEditor
    },
    data() {
        return {
            localValue: undefined as any,
            textareaHeight: "50px",
            showMediaViewer: false,
            mediaViewerConfig: null as MediaViewerConfig | null,
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
        schema() {
            return this.$store.state.schema
        },
        convertDurationToSeconds() {
            return moment.duration(this.localValue).asSeconds()
        },
        convertSecondsToDuration() {
            return secondsToISO8601Duration(this.localValue)
        },
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
        },
        arrayInputType() {
            // TODO - for things like arrays of integers, we need to look at
            // the subtype and not just the format.
            if (this.format == "date") {
                return "date"
            } else if (this.format == "date-time") {
                return "datetime-local"
            } else if (this.format == "time") {
                return "time"
            } else {
                return "text"
            }
        }
    },
    methods: {
        setTextareaHeight() {
            let element = this.$refs.textarea as HTMLTextAreaElement
            if (element) {
                if (element.scrollHeight > element.clientHeight) {
                    const cursorPosition = element.selectionStart
                    this.textareaHeight = element.scrollHeight + "px"
                    window.setTimeout(() => {
                        element.setSelectionRange(
                            cursorPosition,
                            cursorPosition
                        )
                    }, 0)
                }
            }
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
        formatJSON(value: string): string {
            return JSON.stringify(JSON.parse(value), null, 2)
        },
        async uploadFile(event: Event) {
            const target = event.target as HTMLInputElement
            const file = target.files?.[0]

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
                        this.localValue = [
                            ...this.localValue,
                            response.data.file_key
                        ]
                    } else {
                        this.localValue = [response.data.file_key]
                    }
                } else {
                    this.localValue = response.data.file_key
                }
            } catch (error) {
                let errorMessage = "The request failed."

                if (axios.isAxiosError(error) && error.response) {
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
                }

                let message: APIResponseMessage = {
                    contents: errorMessage,
                    type: "error"
                }
                this.$store.commit("updateApiResponseMessage", message)
            }

            target.value = ""
            this.showLoadingOverlay = false
        },
        setLocalValue(value: any) {
            if (this.widget == "json") {
                this.localValue = value ? this.formatJSON(value) : null
            } else {
                this.localValue = value
            }

            let app = this

            setTimeout(function () {
                app.setTextareaHeight()
            }, 0)
        }
    },
    watch: {
        value(newValue) {
            this.setLocalValue(newValue)
        },
        currentTableName() {
            this.localValue = undefined
        }
    },
    mounted() {
        this.setLocalValue(this.value)
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
