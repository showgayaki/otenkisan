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
            currentDate: 'Datetime',
            currentTime: ['Loading...'],
            week: ['(日)', '(月)', '(火)', '(水)', '(木)',  '(金)', '(土)'],
        }
    },
    mounted: function(){
        let timerId = setInterval(this.getDatetimeNow, 1000);
    },
    methods: {
        getDatetimeNow(){
            const now: Date = new Date;
            const year = String(now.getFullYear());
            const month = String(now.getMonth() + 1);
            const date = String(now.getDate());
            const day = this.week[now.getDay()];

            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');

            this.currentDate = year + '年' + month + '月' + date + '日' + day;
            this.currentTime = [hours, minutes, seconds];

            // 親コンポーネントに日時を渡す
            this.$emit(
                'fetchTime',
                {
                    'year': year,
                    'month': month,
                    'date': date,
                    'day': day,
                    'hours': hours,
                    'minutes': minutes,
                    'seconds': seconds
                }
            );
        }
    }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.datetime-now{
    margin-bottom: 10px;
    &__date{
        margin-bottom: 10px;
        font-size: 40px;
    }
    &__clock{
        font-family: "MPLUS1p-Medium";
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
        margin-bottom: 20px;
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
