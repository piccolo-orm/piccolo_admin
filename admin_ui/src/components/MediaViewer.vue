<template>
    <div id="media_viewer">
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

        <div
            class="image_container"
            v-bind:style="{ backgroundImage: `url(${fileURL})` }"
        ></div>

        <div class="bottom_bar">
            <p>
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
import Vue from "vue"
import { PropType } from "vue"

import { MediaViewerConfig } from "@/interfaces"

// @ts-ignore
const BASE_URL = process.env.VUE_APP_BASE_URI

export default Vue.extend({
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
        padding: 1rem;
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

            span {
                font-weight: bold;
            }
        }

        p.close {
            padding-left: 1rem;
            flex-shrink: 0;

            a {
                color: white;
                font-size: 2rem;
            }
        }
    }

    div.image_container {
        flex-grow: 1;
        flex-shrink: 1;
        background-size: contain;
        background-position: center center;
        background-repeat: no-repeat;
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
