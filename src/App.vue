<template>
    <div class="container">
        <DatetimeNow :currentDate="currentDate" :currentTime="currentTime" />
        <div class="weather-calendar">
            <div class="weather-calendar__forecast-temp">
                <WeatherForecast :minutes="datetime['minutes']" :seconds="datetime['seconds']" />
                <SwitchBot :seconds="datetime['seconds']" />
            </div>
            <MonthlyCalendar :datetime="datetime" :holidaysDate="holidaysDate"/>
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
import ApiService from '@/services/ApiService';
import ResponseData from '@/types/ResponseData';
import Holidays from '@/types/Holidays';

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
                isSaturday: false,
                isHoliday: false,
            },
            currentDate: {},
            currentTime: ['Loading...'],
            week: ['日', '月', '火', '水', '木', '金', '土'],
            holidaysDate: {} as Holidays,
            loading: true,
            errored: false,
            errorText: '',
        };
    },
    mounted: function(){
        this.fetchHolidaysDate();
        let timerId = setInterval(this.getDatetimeNow, 1000);
    },
    methods: {
        // 現在時刻取得
        getDatetimeNow(){
            const now: Date = new Date;
            this.datetime['year'] = String(now.getFullYear());
            this.datetime['month'] = String(now.getMonth() + 1);
            this.datetime['date'] = String(now.getDate());
            this.datetime['day'] = this.week[now.getDay()];
            this.datetime['hours'] = String(now.getHours()).padStart(2, '0');
            this.datetime['minutes'] = String(now.getMinutes()).padStart(2, '0');
            this.datetime['seconds'] = String(now.getSeconds()).padStart(2, '0');
            this.datetime['isSaturday'] = (now.getDay() == 6)? true: false;

            // 2022-01-01の形にして比較、日曜 or 祝日かどうか判定
            let dateNow = this.datetime['year'] + '-' + this.datetime['month'] + '-' + this.datetime['date'];
            this.datetime['isHoliday'] = (now.getDay() == 0 || dateNow in this.holidaysDate)? true: false;

            this.currentDate = {
                'year': this.datetime['year'],
                'month': this.datetime['month'],
                'date': this.datetime['date'],
                'day': this.datetime['day'],
                'isHoliday': this.datetime['isHoliday'],
                'isSaturday': this.datetime['isSaturday'],
            };
            this.currentTime = [this.datetime['hours'], this.datetime['minutes'], this.datetime['seconds']];
        },
        // 祝日情報取得
        fetchHolidaysDate(){
            ApiService.getAll('holiday.json')
            .then((res: ResponseData) => {
                this.errored = false;
                this.holidaysDate = res.data;
                console.log(res.data);
            })
            .catch(error => {
                console.log(error);
                this.errored = true;
                this.errorText = error;
            })
            .finally(() => this.loading = false)
        },
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
        padding: 20px;
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
