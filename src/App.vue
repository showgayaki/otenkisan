<template>
    <div class="container">
        <DatetimeNow />
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import '../src/assets/css/reset.css'
import DatetimeNow from '@/components/DatetimeNow.vue';

export default defineComponent({
    name: 'App',
    components: {
        DatetimeNow,
    },
});
</script>

<style lang="scss">
@font-face {
   font-family: "MPLUS1p-Regular";
   src: url('assets/fonts/MPLUS1p-Regular.ttf') format("truetype");
}
@font-face {
   font-family: "MPLUS1p-Medium";
   src: url('assets/fonts/MPLUS1p-Medium.ttf') format("truetype");
}
#app{
    height: 100%;
    font-family: Avenir, "MPLUS1p-Regular";
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #fff;
}
html{
    height: 100%;
    background: #333;
}
.container{
    padding: 30px 15px;
    margin: 0 auto;
    @media screen and (min-width: 576px){
        padding: 15px;
    }
    @media screen and (min-width: 960px){
        padding: 20px;
    }
}
</style>
