<template>
    <div class="weather-forecast">
        <p v-if="errored" class="weather-forecast__error">{{ errorText }}</p>
        <p class="weather-forecast__check-time">{{ checkTime }}</p>
        <div class="weather-forecast__forecast">
            <div class="weather-forecast__sky-pattern">
                <img v-bind:src="weatherForecast['icon']" class="weather-forecast__icon" alt="天気アイコン">
                <p class="weather-forecast__state">{{ weatherForecast['state'] }}</p>
            </div>
            <div class="weather-forecast__temp-wrap">
                <p class="weather-forecast__temp weather-forecast__temp--max">
                    <span class="weather-forecast__temp-text">最高</span>
                    <span class="weather-forecast__degree">{{ weatherForecast['max'] }}</span>
                    <span class="weather-forecast__temp-diff">{{ weatherForecast['max_diff'] }}</span>
                </p>
                <p class="weather-forecast__temp weather-forecast__temp--min">
                    <span class="weather-forecast__temp-text">最低</span>
                    <span class="weather-forecast__degree"> {{ weatherForecast['min'] }}</span>
                    <span class="weather-forecast__temp-diff">{{ weatherForecast['min_diff'] }}</span>
                </p>
            </div>
        </div>
        <table class="weather-forecast__table">
            <thead>
                <tr>
                    <th v-for="span in timeSpan" :key="span" class="weather-forecast__table-header">{{ span }}</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td v-for="percent in weatherForecast['rainy_percent']" :key="percent" class="weather-forecast__table-data">{{ percent }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ApiService from "@/services/ApiService";
import ResponseData from "@/types/ResponseData";
import WeatherForecast from '@/types/Weather';

export default defineComponent({
    name: 'WeatherForecast',
    props: [
        'minutes',
        'seconds'
    ],
    data() {
        return{
            timeSpan: ['0-6', '6-12', '12-18', '18-24'],
            weatherForecast: {
                'state': '---',
                'max': '---',
                'max_diff': '[---]',
                'min': '---',
                'min_diff': '[---]',
                'icon': 'https://static.tenki.jp/images/icon/forecast-days-weather/01_n.png',
                'rainy_percent': [
                    '---',
                    '---',
                    '---',
                    '---'
                ]
            } as WeatherForecast,
            loading: true,
            errored: false,
            errorText: '',
        }
    },
    mounted: function(){
        this.fetchWeatherForecast();
    },
    computed: {
        checkTime(){
            // 一時間に一回、指定分に実行
            if(this.minutes == process.env.VUE_APP_FETCH_API_MINUTES && this.seconds == '00'){
                this.fetchWeatherForecast();
            }
            return {'minutes': this.minutes, 'seconds': this.seconds};
        }
    },
    methods: {
        // 参考：https://www.bezkoder.com/vue-3-typescript-axios/
        fetchWeatherForecast(){
            ApiService.getAll('forecast.json')
            .then((res: ResponseData) => {
                console.log(res.data);
                this.errored = false;
                this.weatherForecast = res.data;
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
.weather-forecast{
    width: 100%;
    margin: 0 20px 25px 0;
    &__error{
        font-size: 16px;
        text-align: center;
    }
    &__check-time{
        display: none;
    }
    &__forecast{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
        font-size: 16px;
    }
    &__sky-pattern{
        margin: 0 20px 0 0;
        text-align: center;
    }
    &__icon{
        width: 120px;
    }
    &__temp{
        &--max{
            margin-bottom: 5px;
            color: #f00;
        }
        &--min{
            color: #0096FF;
        }
    }
    &__temp-text{
        display: inline-block;
        width: 3em;
    }
    &__degree{
        width: 6rem;
        display: inline-block;
        font-size: 28px;
        font-weight: bold;
        text-align: right;
        &::after{
            display: inline-block;
            content: "℃";
            margin: 0 8px;
            font-size: 27px;
        }
    }
    &__table{
        width: 100%;
    }
    &__table,
    &__table-header,
    &__table-data{
        border: 1px solid #fff;
        font-size: 16px;
    }
    &__table-header,
    &__table-data{
        width: calc(100% / 4);
        padding: 6px 0;
        text-align: center;
    }
    &__icon{
        width: 80px;
    }
    &__temp-text{
        width: 2em;
    }
    @media screen and (min-width: 576px){
        // margin: 0 20px 0 0;
    }
    @media screen and (min-width: 960px){
        &__error{
            font-size: 24px;
        }
        &__forecast{
            margin-bottom: 10px;
            font-size: 27px;
        }
        &__sky-pattern{
            margin: 0 20px 0 0;
        }
        &__icon{
            width: 180px;
        }
        &__state{
            margin-top: -15px;
        }
        &__temp-text{
            width: 3em;
        }
        &__degree{
            font-size: 36px;
        }
        &__table{
            width: 100%;
        }
        &__table,
        &__table-header,
        &__table-data{
            border: 1px solid #fff;
            font-size: 24px;
        }
        &__table-header,
        &__table-data{
            width: calc(100% / 4);
            padding: 8px 0;
            text-align: center;
        }
    }
}
</style>
