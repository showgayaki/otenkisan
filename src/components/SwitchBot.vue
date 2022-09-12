<template>
    <div class="switchbot">
        <p v-if="errored" class="switchbot__error">{{ errorText }}</p>
        <p class="switchbot__check-time">{{ checkTime }}</p>
        <table v-if="!('error' in switchBot)" class="switchbot__table">
            <thead>
                <tr>
                    <th v-for="header in switchbotHeader" :key="header" class="switchbot__table-header">{{ header }}</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td v-for="sbData in switchBot" :key="sbData" class="switchbot__table-data">{{ sbData }}</td>
                </tr>
            </tbody>
        </table>
        <table v-else class="switchbot__table">
            <thead>
                <tr>
                    <th class="switchbot__table-header">エラー</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="switchbot__table-data switchbot__table-data--error">{{ switchBot.error }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import ApiService from "@/services/ApiService";
import ResponseData from "@/types/ResponseData";
import SwitchBot from '@/types/SwitchBot';

export default defineComponent({
    name: 'SwitchBot',
    props: [
        'seconds',
    ],
    data() {
        return{
            switchbotHeader: ['室温', '湿度'],
            switchBot: {} as SwitchBot,
            loading: true,
            errored: false,
            errorText: '',
        }
    },
    mounted: function(){
        this.fetchSwitchbotData();
    },
    computed: {
        checkTime(){
            // 1分ごとに実行
            if(this.seconds == '00'){
                this.fetchSwitchbotData();
            }
            return this.seconds;
        }
    },
    methods: {
        fetchSwitchbotData(){
            ApiService.getAll('switchbot.json')
            .then((res: ResponseData) => {
                if(!('error' in res.data)){
                    res.data['temperature'] = String(res.data['temperature']) + '℃';
                    res.data['humidity'] = String(res.data['humidity']) + '%';
                    this.errored = false;
                }
                this.switchBot = res.data;
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
.switchbot{
    margin-bottom: 30px;
    &__check-time{
        display: none;
    }
    &__table{
        width: 100%;
        table-layout: fixed;
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
        padding: 6px;
        text-align: center;
        &--error{
            white-space: nowrap;
            overflow: auto;
        }
    }
    @media screen and (min-width: 576px){
    }
    @media screen and (min-width: 960px){
        margin-bottom: 0;
        &__table,
        &__table-header,
        &__table-data{
            font-size: 24px;
        }
    }
}
</style>
