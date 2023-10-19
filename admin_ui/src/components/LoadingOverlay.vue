<template>
    <div class="loading_overlay">
        <p>
            <font-awesome-icon
                icon="circle-notch"
                class="fa-spin"
            ></font-awesome-icon
            >{{ message }}
        </p>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

export default defineComponent({
    props: {
        message: {
            type: String as PropType<string>,
            default: "Uploading file"
        }
    }
})
</script>

<style scoped lang="less">
div.loading_overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    p {
        color: white;
        text-align: center;

        svg {
            margin: 0 0.5rem 0 0;
            padding: 0;
        }
    }
}
</style>
