<template>
    <div class="password_wrapper">
        <input
            name="password"
            v-bind:value="value"
            v-bind:type="showPassword ? 'text' : 'password'"
            v-on:input="
                $emit('input', ($event.target as HTMLInputElement).value)
            "
        />
        <span
            class="viewer"
            v-if="value"
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
import { defineComponent } from "vue"

export default defineComponent({
    emits: ["input"],
    props: {
        value: String
    },
    data() {
        return {
            showPassword: false
        }
    }
})
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
