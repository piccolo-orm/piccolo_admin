<template>
    <div id="overlay">
        <div class="modal opaque">
            <div class="heading">
                <h1>{{ title }}</h1>

                <p class="close">
                    <a
                        class="subtle"
                        href="#"
                        v-on:click.prevent="$emit('close')"
                    >
                        <font-awesome-icon icon="times" />
                    </a>
                </p>
            </div>

            <slot></slot>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
    props: {
        title: {
            type: String,
            default: ""
        }
    }
})
</script>

<style scoped lang="less">
div#overlay {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.7);
    overflow: auto;
    z-index: 2000;

    div.modal {
        border-radius: 0.5rem;
        box-sizing: border-box;
        margin: 1rem auto;
        max-width: 100%;
        padding: 1rem;
        width: 30rem;

        label,
        input {
            width: 100%;
            display: block;
        }

        div.heading {
            display: flex;
            flex-direction: row;
            align-items: center;

            h1 {
                flex-grow: 1;
                font-size: 1.2rem;
            }
        }
    }
}
</style>
