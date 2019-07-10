<template>
<div class="home">
    <Admin />
</div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Admin from '@/components/Admin.vue';

@Component({
    components: {
        Admin,
    },
})
export default class Home extends Vue {}
</script>
