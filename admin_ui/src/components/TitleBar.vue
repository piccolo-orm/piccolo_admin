<template>
    <div class="title_bar">
        <div class="title">
            <h1>
                {{ title }}
            </h1>
            <Tooltip v-if="titleTooltip" :content="titleTooltip" />
        </div>
        <div class="buttons">
            <slot name="buttons"></slot>
        </div>
    </div>
</template>

<script>
import Tooltip from "./Tooltip.vue"

export default {
    props: {
        title: {
            type: String,
            default: undefined,
        },
        titleTooltip: {
            type: String,
            default: undefined,
        },
    },
    components: {
        Tooltip,
    },
}
</script>

<style lang="less">
@import "../vars.less";

div.title_bar {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 0.5rem 0;

    @media (max-width: @mobile_width) {
        align-items: initial;
        flex-direction: column;
    }

    div.title {
        flex-grow: 1;
        display: flex;
        align-items: center;

        h1 {
            display: inline-block;
            text-transform: capitalize;
            margin: 0 0.5rem 0 0;
        }
    }

    p {
        flex-grow: 0;
    }

    div.buttons {
        box-sizing: border-box;
        cursor: pointer;
        display: flex;
        flex-direction: row;

        @media (max-width: @mobile_width) {
            width: 100%;
        }

        a.button {
            display: block;
            flex-grow: 0;
            font-weight: bold;
            text-decoration: none;
            margin-left: 0.25rem;
            box-sizing: border-box;
            padding: 0.2rem 0.5rem;
            text-align: center;

            @media (max-width: @mobile_width) {
                flex-grow: 1;

                svg {
                    padding: 0 !important;
                }
            }

            span {
                @media (max-width: @mobile_width) {
                    display: block;
                }
            }

            &:first-child {
                margin-left: 0;
            }
        }
    }
}
</style>
