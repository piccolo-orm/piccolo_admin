<template>
    <div id="media_viewer" v-if="mediaViewerConfig">
        <!-- Top bar -->

        <div class="top_bar">
            <p class="file_key">
                <span>File:</span> {{ mediaViewerConfig.fileKey }}
            </p>

            <p class="close">
                <a href="#" @click.prevent="$emit('close')"
                    ><font-awesome-icon icon="times"></font-awesome-icon
                ></a>
            </p>
        </div>

        <!-- Media containers -->

        <template v-if="fileURL">
            <div
                v-if="isImage(mediaViewerConfig.fileKey)"
                class="image_container"
            >
                <img :src="fileURL" />
            </div>

            <div
                v-else-if="isVideo(mediaViewerConfig.fileKey)"
                class="video_container"
            >
                <video controls :src="fileURL">
                    Video playback not available
                </video>
            </div>

            <div
                v-else-if="isAudio(mediaViewerConfig.fileKey)"
                class="audio_container"
            >
                <audio controls :src="fileURL">
                    Audio playback not available
                </audio>
            </div>

            <div
                v-else-if="isPDF(mediaViewerConfig.fileKey)"
                class="pdf_container"
            >
                <iframe :src="fileURL"></iframe>
            </div>

            <div class="no_preview" v-else>
                <p>
                    <font-awesome-icon icon="file"></font-awesome-icon> Unable
                    to preview file - download below.
                </p>
            </div>
        </template>

        <div v-else class="loading_container">
            <p>
                <font-awesome-icon
                    icon="circle-notch"
                    class="fa-spin"
                ></font-awesome-icon
                >Loading ...
            </p>
        </div>

        <!-- Bottom bar -->

        <div class="bottom_bar">
            <p v-if="fileURL">
                <a class="button" :href="fileURL" download
                    ><font-awesome-icon icon="download"></font-awesome-icon>
                    Download</a
                >
            </p>
        </div>
    </div>
</template>

<script lang="ts">
import axios from "axios"
import { defineComponent, type PropType } from "vue"

import type { MediaViewerConfig } from "@/interfaces"

const BASE_URL = import.meta.env.VITE_APP_BASE_URI

const AUDIO_EXTENSIONS = ["mp3", "wav"]
const IMAGE_EXTENSIONS = ["gif", "jpeg", "jpg", "png", "svg", "tif", "webp"]
const VIDEO_EXTENSIONS = ["mp4", "webm"]

export default defineComponent({
    props: {
        mediaViewerConfig: {
            type: Object as PropType<MediaViewerConfig>
        }
    },
    data() {
        return {
            fileURL: null
        }
    },
    methods: {
        isAudio(fileKey: string): boolean {
            const components = fileKey.split(".")
            const extension = components[components.length - 1].toLowerCase()
            return AUDIO_EXTENSIONS.indexOf(extension) != -1
        },
        isImage(fileKey: string): boolean {
            const components = fileKey.split(".")
            const extension = components[components.length - 1].toLowerCase()
            return IMAGE_EXTENSIONS.indexOf(extension) != -1
        },
        isPDF(fileKey: string): boolean {
            const components = fileKey.split(".")
            const extension = components[components.length - 1].toLowerCase()
            return extension.toLowerCase() == "pdf"
        },
        isVideo(fileKey: string): boolean {
            const components = fileKey.split(".")
            const extension = components[components.length - 1].toLowerCase()
            return VIDEO_EXTENSIONS.indexOf(extension) != -1
        },
        async generateFileURL({
            columnName,
            tableName,
            fileKey
        }: MediaViewerConfig) {
            const response = await axios.post(
                `${BASE_URL}media/generate-file-url/`,
                {
                    column_name: columnName,
                    table_name: tableName,
                    file_key: fileKey
                }
            )
            return response.data["file_url"]
        }
    },
    watch: {
        async mediaViewerConfig(mediaViewerConfig: MediaViewerConfig) {
            if (mediaViewerConfig) {
                this.fileURL = await this.generateFileURL(mediaViewerConfig)
            }
        }
    },
    async mounted() {
        if (this.mediaViewerConfig) {
            this.fileURL = await this.generateFileURL(this.mediaViewerConfig)
        }
    }
})
</script>

<style lang="less">
div#media_viewer {
    background-color: rgba(0, 0, 0, 0.8);
    left: 0;
    position: fixed;
    right: 0;
    top: 0;
    display: flex;
    flex-direction: column;
    height: 100vh;

    div.top_bar {
        flex-grow: 0;
        flex-shrink: 0;
        display: flex;
        flex-direction: row;
        padding: 0.5rem;
        align-items: center;

        p {
            margin: 0;
            padding: 0;
        }

        p.file_key {
            color: white;
            flex-grow: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: center;
            white-space: nowrap;
            font-size: 0.9em;
            padding: 0 0.5rem;

            span {
                font-weight: bold;
            }
        }

        p.close {
            flex-shrink: 0;

            a {
                color: white;
                font-size: 2rem;
            }
        }
    }

    div.audio_container,
    div.image_container,
    div.pdf_container,
    div.video_container,
    div.no_preview,
    div.loading_container {
        flex-grow: 1;
        flex-shrink: 1;
    }

    div.pdf_container {
        iframe {
            border: none;
            width: 100%;
            height: 100%;
        }
    }

    div.audio_container {
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: center;

        audio {
            max-width: 100%;
        }
    }

    div.loading_container {
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: center;

        p {
            text-align: center;

            svg {
                padding: 0;
                margin-right: 0.5rem;
            }
        }
    }

    div.image_container,
    div.video_container {
        position: relative;

        video,
        img {
            max-height: 100%;
            max-width: 100%;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            margin: auto auto;
        }
    }

    div.no_preview {
        display: flex;
        align-items: center;

        p {
            text-align: center;
            flex-grow: 1;
        }
    }

    div.bottom_bar {
        flex-grow: 0;
        flex-shrink: 0;

        p {
            text-align: center;

            a {
                text-decoration: none;
            }
        }
    }
}
</style>
