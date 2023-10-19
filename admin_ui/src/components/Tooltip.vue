<template>
    <span class="tooltip">
        <a
            href="#"
            v-on:click.prevent="popupVisible ? hidePopup() : showPopup($event)"
            v-on:blur="hidePopup()"
            title="Click for more info"
        >
            <font-awesome-icon icon="question-circle" />
        </a>

        <div
            class="popup"
            v-show="popupVisible"
            :style="{
                top: popupTop,
                bottom: popupBottom,
                right: popupRight,
                left: popupLeft,
                width: popupWidth,
                textAlign: textAlign
            }"
        >
            <span>{{ content }}</span>
        </div>
    </span>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
    props: {
        content: {
            default: "",
            type: String
        }
    },
    data() {
        return {
            popupVisible: false,
            popupTop: "auto",
            popupBottom: "auto",
            popupLeft: "auto",
            popupRight: "auto",
            popupWidth: "50px",
            textAlign: "left" as "left" | "right" | "center",
            onResize: undefined as (() => void) | undefined
        }
    },
    methods: {
        showPopup(event: MouseEvent) {
            const scrollHeight = document.body.scrollHeight
            const scrollWidth = document.body.scrollWidth
            const eventY = event.pageY
            const eventX = event.pageX

            if (eventX < 150) {
                console.log("Right")
                this.popupLeft = eventX + 20 + "px"
                this.popupRight = "auto"
                this.popupWidth = scrollWidth - eventX - 20 + "px"
                this.textAlign = "left"
            } else if (scrollWidth - eventX < 150) {
                console.log("Left")
                this.popupLeft = "auto"
                this.popupRight = eventX - 20 + "px"
                this.popupWidth = eventX - 20 + "px"
                this.textAlign = "right"
            } else {
                console.log("Center")
                this.popupWidth = "300px"
                this.popupLeft = eventX - 150 + "px"
                this.popupRight = "auto"
                this.textAlign = "center"
            }

            if (scrollHeight - eventY < 300) {
                console.log("Above")
                this.popupBottom = scrollHeight - eventY + 20 + "px"
                this.popupTop = "auto"
            } else {
                console.log("Below")
                this.popupBottom = "auto"
                this.popupTop = eventY + 20 + "px"
            }

            this.popupVisible = true
        },
        hidePopup() {
            this.popupVisible = false
        }
    },
    mounted() {
        let app = this
        function onResize() {
            app.popupVisible = false
        }
        this.onResize = onResize
        window.addEventListener("resize", onResize)
    },
    destroyed() {
        if (this.onResize) {
            window.removeEventListener("resize", this.onResize)
        }
    }
})
</script>

<style lang="less">
@import "../vars.less";

span.tooltip {
    color: @light_blue;
    display: inline-block;
    font-size: 0.9rem;
    z-index: 100;

    div.popup {
        display: block;
        position: absolute;
        max-width: 100%;

        span {
            display: inline-block;
            border-radius: 0.2rem;
            box-shadow: 1px 1px 1px rgba(0, 0, 0, 0.5);
            box-sizing: border-box;
            padding: 0.5rem;
        }
    }
}
.dark_mode .popup span {
    background-color: white;
    color: @dark_grey;
}

.light_mode .popup span {
    background-color: @dark_grey;
    color: white;
}
</style>
