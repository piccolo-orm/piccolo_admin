<template>
    <div class="password_wrapper">
        <input
            name="password"
            v-model="password"
            v-bind:type="showPassword ? 'text' : 'password'"
            v-on:input="passwordValue"
        />
        <span
            class="viewer"
            v-if="password"
            v-on:click="showPassword = !showPassword"
        >
            <font-awesome-icon
                v-if="!showPassword"
                icon="eye"
                title="Show password"
            />
            <font-awesome-icon v-else icon="eye-slash" title="Hide password" />
        </span>
    </div>
</template>

<script lang="ts">
export default {
    props: {
        showPassword: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            password: ""
        }
    },
    methods: {
        passwordValue() {
            this.$emit("input", this.password)
        }
    }
}
</script>

<style lang="less">
div.password_wrapper {
    position: relative;

    span.viewer {
        color: #878787;
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        z-index: 1;
        cursor: pointer;
    }
}
</style>