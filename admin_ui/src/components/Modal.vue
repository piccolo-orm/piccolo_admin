<template>
    <div id="overlay">
        <div class="modal opaque">
            <p class="close">
                <a
                    href="#"
                    v-on:click.prevent="$emit('close')"
                >
                    <font-awesome-icon icon="times" />
                </a>
            </p>

            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {}
</script>

<style scoped lang="less">
div#overlay {
    position: absolute;
    top: 0%;
    left: 0%;
    height: 100%;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.7);

    div.modal {
        width: 30rem;
        margin: 1rem auto;
        box-sizing: border-box;
        padding: 1rem;
        border-radius: 0.5rem;

        label,
        input {
            width: 100%;
            display: block;
        }

        p.close {
            text-align: right;
        }
    }
}
</style>
