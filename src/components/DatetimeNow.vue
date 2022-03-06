<template>
    <div class="datetime-now">
        <h1 class="datetime-now__date">{{ currentDate }}</h1>
        <p class="datetime-now__clock">
            <span v-for="time in currentTime" :key="time" class="datetime-now__time">{{ time }}</span>
        </p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'DatetimeNow',
    data(){
        return{
            currentDate: '',
            currentTime: [] as string[],
            week: ['(日)', '(月)', '(火)', '(水)', '(木)',  '(金)', '(土)'],
        }
    },
    mounted: function(){
        let timerId = setInterval(this.getDatetimeNow, 1000);
    },
    methods: {
        getDatetimeNow(){
            const now: Date = new Date;
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');

            this.currentDate = now.getFullYear() + '年' + (now.getMonth() + 1) + '月' + now.getDate() + '日' + this.week[now.getDay()];
            this.currentTime = [hours, minutes, seconds]
        }
    }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.datetime-now{
    margin-bottom: 30px;
    &__date{
        margin-bottom: 30px;
        font-size: 65px;
    }
    &__clock{
        font-size: 120px;
        text-align: center;
    }
    &__time{
        color: #fff;
        &:not(:last-child)::after{
            content: ":";
            display: inline-block;
        }
    }

    @media screen and (max-width: 768px){
        &__date{
            margin-bottom: 30px;
            font-size: 24px;
        }
        &__clock{
            font-size: 60px;
        }
    }
}
</style>
