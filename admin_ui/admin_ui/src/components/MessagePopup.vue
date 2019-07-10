<template>
<div id="message_popup" v-if="visible">
    <p class="message">{{ message }}</p>
    <p class="close"><a href="#" v-on:click.prevent="visible = false">Close</a></p>
</div>
</template>


<script lang="ts">
import Vue from 'vue'
import * as i from '../interfaces'

export default Vue.extend({
    data: function() {
        return {
            visible: false
        }
    },
    computed: {
        message: function(): string {
            return this.apiResponseMessage ? this.apiResponseMessage.contents : '-'
        },
        apiResponseMessage: function(): i.APIResponseMessage {
            return this.$store.state.apiResponseMessage
        }
    },
    watch: {
        apiResponseMessage: function() {
            this.visible = true
            let app = this
            setTimeout(
                function() {
                    app.visible = false
                },
                3000
            )
        }
    }
})
</script>


<style lang="less">
div#message_popup {
    display: flex;
    position: fixed;
    bottom: 0;
    width: 100%;
    padding: 0.5rem 1rem;
    box-sizing: border-box;
    background-color: green;

    p.message {
        flex-grow: 1;
        text-align: center;
    }

    p.close {
        flex-grow: 0;
    }
}
</style>
