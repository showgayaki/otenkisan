<template>
    <div class="datetime-now">
        <h1 class="datetime-now__date date" v-if="Object.keys(currentDate).length">
            <span class="date__year">{{ currentDate.year }}年</span>
            <span class="date__month">{{ currentDate.month }}月</span>
            <span class="date__date">{{ currentDate.date }}日</span>
            <span class="date__day date__day--holiday" v-if="currentDate.isHoliday">{{ currentDate.day }}</span>
            <span class="date__day date__day--saturday" v-else-if="currentDate.isSaturday">{{ currentDate.day }}</span>
            <span class="date__day" v-else>{{ currentDate.day }}</span>
        </h1>
        <h1 class="datetime-now__date" v-else>
            Datetime
        </h1>
        <p class="datetime-now__clock">
            <span v-for="time in currentTime" :key="time" class="datetime-now__time">{{ time }}</span>
        </p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'DatetimeNow',
    props: [
        'currentDate',
        'currentTime'
    ],
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
            color: #00f;
        }
    }
}
</style>
