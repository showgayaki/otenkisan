<template>
    <div class="weather-forecast">
        <div class="weather-forecast__forecast">
            <div class="weather-forecast__sky-pattern">
                <img v-bind:src="weatherForecast['icon']" class="weather-forecast__icon" alt="天気アイコン">
                <p class="weather-forecast__state">{{ weatherForecast['state']}}</p>
            </div>
            <div class="weather-forecast__temp-wrap">
                <p class="weather-forecast__temp weather-forecast__temp--max">
                    <span class="weather-forecast__temp-text">最高</span>
                    <span class="weather-forecast__degree">{{ weatherForecast['max']}}</span>
                    <span class="weather-forecast__temp-text">{{ weatherForecast['max-diff']}}</span>
                </p>
                <p class="weather-forecast__temp weather-forecast__temp--min">
                    <span class="weather-forecast__temp-text">最低</span>
                    <span class="weather-forecast__degree"> {{ weatherForecast['min']}}</span>
                    <span class="weather-forecast__temp-text">{{ weatherForecast['min-diff']}}</span>
                </p>
            </div>
        </div>
        <table class="weather-forecast__table">
            <thead>
                <tr>
                    <th class="weather-forecast__table-header">0-6</th><th class="weather-forecast__table-header">6-12</th><th class="weather-forecast__table-header">12-18</th><th class="weather-forecast__table-header">18-24</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td v-for="percent in weatherForecast['rainy-percent']" :key="percent" class="weather-forecast__table-data">{{ percent }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import weatherForecast from '../assets/json/temp.json';

export default defineComponent({
    name: 'WeatherForecast',
    data(){
        return{
            weatherForecast: weatherForecast,
        }
    },
    mounted: function(){
        this.splitTemperture();
    },
    methods: {
        splitTemperture(){
            let tempMax = this.weatherForecast['max'].split('℃')[0];
            let tempMaxDiff = '℃' + this.weatherForecast['max'].split('℃')[1];
            this.weatherForecast['max'] = tempMax;
            this.weatherForecast['max-diff'] = tempMaxDiff;

            let tempMin = this.weatherForecast['min'].split('℃')[0];
            let tempMinDiff = '℃' + this.weatherForecast['min'].split('℃')[1];
            this.weatherForecast['min'] = tempMin;
            this.weatherForecast['min-diff'] = tempMinDiff;
        }
    }
});
</script>

<style lang="scss">
.weather-forecast{
    width: calc(50% - 25px);
    margin-right: 50px;
    &__forecast{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        font-size: 27px;
    }
    &__sky-pattern{
        margin: 0 50px 0 0;
        text-align: center;
    }
    &__icon{
        width: 120px;
        margin-bottom: 20px;
    }
    &__temp{
        &--max{
            margin-bottom: 10px;
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
        width: 3rem;
        display: inline-block;
        font-size: 34px;
        font-weight: bold;
        text-align: right;
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
    @media screen and (max-width: 768px){
    }
}
</style>
