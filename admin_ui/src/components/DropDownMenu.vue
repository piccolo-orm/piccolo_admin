<template>
    <ul id="drop_down_menu">
        <slot />
    </ul>
</template>

<script setup lang="ts"></script>

<style lang="less">
@import "../vars.less";

ul#drop_down_menu {
    background-color: darken(@dark_grey, 5%);
    box-shadow: 1px 5px 9px 2px rgba(0, 0, 0, 0.5);
    list-style: none;
    padding: 0;
    position: absolute;
    top: 100%;
    right: 0;
    width: 15rem;
    margin-top: 0.5rem;
    z-index: 2000;

    li {
        margin: 0 !important;
        text-align: center;
        width: 100%;

        &:hover {
            background-color: rgba(255, 255, 255, 0.1);
        }

        a {
            color: white !important;
            font-weight: bold;
            display: block;
            padding: 0.5rem 1rem;
            box-sizing: border-box;
        }
    }
}
</style>
