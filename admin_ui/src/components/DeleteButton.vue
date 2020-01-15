<template>
    <a
        href="#"
        id="delete"
        title="Delete Row"
        v-on:click.prevent="$emit('triggered')"
    >
        <font-awesome-icon icon="trash-alt" />
    </a>
</template>

<script>
export default {}
</script>

<style scoped lang="less">
@import "../vars.less";

@keyframes shake {
    0% {
        transform: rotate(0deg);
    }
    50% {
        transform: rotate(-10deg);
    }
    100% {
        transform: rotate(10deg);
    }
}

a#delete {
    color: @off_white;
    text-decoration: none;

    &:hover {
        color: @red;

        svg {
            animation: shake 0.4s;
            animation-iteration-count: infinite;
        }
    }
}
</style>
