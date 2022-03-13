<template>
    <div class="container">
        <DatetimeNow @fetchTime="emitTime" />
        <div class="weather-calendar">
            <WeatherForecast :minutes="datetime['minutes']" :seconds="datetime['seconds']" />
            <MonthlyCalendar :datetime="datetime"/>
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
            datetime: {
                year: '',
                month: '',
                date: '',
                day: '',
                hours: '',
                minutes: '',
                seconds: '',
            },
        };
    },
    methods: {
        // DatetimeNowコンポーネントから分と秒を受け取り
        emitTime(datetime: {[index: string]: string}) {
            this.datetime['year'] = datetime['year'];
            this.datetime['month'] = datetime['month'];
            this.datetime['date'] = datetime['date'];
            this.datetime['day'] = datetime['day'];
            this.datetime['hours'] = datetime['hours'];
            this.datetime['minutes'] = datetime['minutes'];
            this.datetime['seconds'] = datetime['seconds'];
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
