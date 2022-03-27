<template>
    <div class="container">
        <DatetimeNow @fetchTime="emitTime" />
        <div class="weather-calendar">
            <div class="weather-calendar__forecast-temp">
                <WeatherForecast :minutes="datetime['minutes']" :seconds="datetime['seconds']" />
                <SwitchBot :seconds="datetime['seconds']" />
            </div>
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
import SwitchBot from '@/components/SwitchBot.vue';

export default defineComponent({
    name: 'App',
    components: {
        DatetimeNow,
        WeatherForecast,
        MonthlyCalendar,
        SwitchBot,
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
        // DatetimeNowコンポーネントから日時を受け取り
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
        padding: 30px;
    }
}
.weather-calendar{
    display: block;
    &__forecast-temp{
        width: 100%;
    }
    @media screen and (min-width: 576px){
        display: flex;
        justify-content: space-between;
        &__forecast-temp{
            width: calc(50% - 15px);
        }
    }
}
</style>
