<template>
    <div class="datetime-now">
        <h1 class="datetime-now__date date" v-if="!(datetime.year == '')">
            <span class="date__year">{{ datetime.year }}年</span>
            <span class="date__month">{{ datetime.month }}月</span>
            <span class="date__date">{{ datetime.date }}日</span>
            <span class="date__day date__day--holiday" v-if="datetime.isHoliday">{{ datetime.day }}</span>
            <span class="date__day date__day--saturday" v-else-if="datetime.isSaturday">{{ datetime.day }}</span>
            <span class="date__day" v-else>{{ datetime.day }}</span>
            <span class="date__day date__day--checktime">{{ checkTime }}</span>
        </h1>
        <h1 class="datetime-now__date" v-else>
            Datetime
        </h1>
        <p class="datetime-now__clock">
            <span v-for="time in currentTime" :key="time" class="datetime-now__time">{{ time }}</span>
        </p>
    </div>
    <div class="weather-calendar">
        <div class="weather-calendar__forecast-temp">
            <WeatherForecast :minutes="datetime['minutes']" :seconds="datetime['seconds']" />
            <SwitchBot :seconds="datetime['seconds']" />
        </div>
        <MonthlyCalendar :datetime="datetime" :holidaysDate="holidaysDate"/>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import WeatherForecast from '@/components/WeatherForecast.vue';
import MonthlyCalendar from '@/components/MonthlyCalendar.vue';
import SwitchBot from '@/components/SwitchBot.vue';
import ApiService from '@/services/ApiService';
import ResponseData from '@/types/ResponseData';
import Holidays from '@/types/Holidays';

export default defineComponent({
    name: 'DatetimeNow',
    components: {
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
        let timerId = setInterval(this.updateTimer, 1000);
    },
    computed: {
        checkTime(){
            // 稼働が長くなると、秒数の描画が１秒ごとじゃなくなってしまうので1時間に一回リロード
            if(this.datetime['minutes'] == '00' && this.datetime['seconds'] == '03'){
                location.reload();
            }
            return false;
        }
    },
    methods: {
        // 現在時刻取得
        updateTimer(){
            const now: Date = new Date;
            let year = now.getFullYear();
            let month = now.getMonth() + 1;
            let date = now.getDate();
            let day = now.getDay();
            let hours = now.getHours();
            let minutes = now.getMinutes();
            let seconds = now.getSeconds();

            // 月・日付は0埋め
            this.datetime['year'] = String(year);
            this.datetime['month'] = String(month).padStart(2, '0');
            this.datetime['date'] = String(date).padStart(2, '0');
            this.datetime['day'] = this.week[now.getDay()];

            // ページ表示時(currentTimeが「Loading...」)か、0時0秒〜0時5秒の間で曜日判定
            if(this.currentTime[0] == 'Loading...' || (hours == 0 && minutes == 0 && seconds < 5)){
                this.datetime['isSaturday'] = (day == 6)? true: false;
                // 2022-01-01の形にして比較、日曜 or 祝日かどうか判定
                let dateNow = this.datetime['year'] + '-' + this.datetime['month'] + '-' + this.datetime['date'];
                this.datetime['isHoliday'] = (day == 0 || dateNow in this.holidaysDate)? true: false;
            }

            // 時間・分・秒は、0埋め
            this.datetime['hours'] = String(hours).padStart(2, '0');
            this.datetime['minutes'] = String(minutes).padStart(2, '0');
            this.datetime['seconds'] = String(seconds).padStart(2, '0');

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
    },
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.datetime-now{
    margin-bottom: 30px;
    &__date{
        margin-bottom: 20px;
        font-size: 22px;
    }
    &__clock{
        font-family: "MPLUS1p-Medium";
        font-size: 60px;
        text-align: center;
        line-height: .8;
    }
    &__time{
        color: #fff;
        &:not(:last-child)::after{
            content: ":";
            display: inline-block;
        }
    }
    @media screen and (min-width: 576px){
        margin-bottom: 15px;
        &__date{
            margin-bottom: 0;
        }
    }
    @media screen and (min-width: 960px){
        margin-bottom: 20px;
        &__date{
            margin-bottom: 20px;
            font-size: 70px;
        }
        &__clock{
            font-size: 150px;
        }
        &__time{
            color: #fff;
            &:not(:last-child)::after{
                content: ":";
                display: inline-block;
            }
        }
    }
}
.date{
    &__day{
        &::before{
            content: "(";
            color: #fff;
        }
        &::after{
            content: ")";
            color: #fff;
        }
        &--holiday{
            color: #f00;
        }
        &--saturday{
            color: #0b8fdb;
        }
        &--checktime{
            display: none;
        }
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
