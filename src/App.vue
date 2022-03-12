<template>
    <div class="container">
        <DatetimeNow @fetchTime="emitTime" />
        <div class="weather-calendar">
            <WeatherForecast :minutes="minutesNow" :seconds="secondsNow" />
            <MonthlyCalendar />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import '../src/assets/css/reset.css'
import DatetimeNow from '@/components/DatetimeNow.vue';
import WeatherForecast from '@/components/WeatherForecast.vue';
import MonthlyCalendar from '@/components/MonthlyCalendar.vue';

export default defineComponent({
    name: 'App',
    components: {
        DatetimeNow,
        WeatherForecast,
        MonthlyCalendar
    },
    data() {
        return {
            minutesNow: '',
            secondsNow: '',
        };
    },
    methods: {
        // DatetimeNowコンポーネントから分と秒を受け取り
        emitTime(time: string[]) {
            this.minutesNow = time[0];
            this.secondsNow = time[1];
        }
    }
});
</script>

<style lang="scss">
#app{
    font-family: Avenir, Helvetica, Arial, sans-serif, "Noto Serif JP";
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #fff;
}
html{
    background: #222;
}
.container{
    padding: 30px;
    margin: 0 auto;
    @media screen and (max-width: 768px){
        display: block;
        padding: 30px 15px;
    }
}
.weather-calendar{
    display: flex;
    @media screen and (max-width: 768px){
        display: block;
    }
}
</style>
