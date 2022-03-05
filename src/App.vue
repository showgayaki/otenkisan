<template>
    <div class="container">
        <DatetimeNow />
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import '../src/assets/css/reset.css'
import DatetimeNow from './components/DatetimeNow.vue';

export default defineComponent({
    name: 'App',
    components: {
        DatetimeNow,
    }
});
</script>

<style>
#app{
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #fff;
}
html{
    background: #000;
}
.container{
    padding: 60px 30px 50px;
    margin: 0 auto;
}
</style>
