
<template>
    <div class="monthly-calendar">
        <p class="monthly-calendar__date">{{ checkDate }}</p>
        <FullCalendar ref="calendar" :options="calendarOptions" />
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import '@fullcalendar/core/vdom';
import FullCalendar, { DayCellContentArg, EventContentArg } from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import holidaysDate from '../../public/json/holiday.json';

export default defineComponent({
    name: 'MonthlyCalendar',
    props: [
        'datetime',
    ],
    components: {
        FullCalendar,
    },
    data(){
        return {
            calendarOptions: {
                plugins: [ dayGridPlugin, interactionPlugin ],
                initialView: 'dayGridMonth',
                locale: 'ja',
                navLinks: false,
                fixedWeekCount: false,
                dayCellContent: function(e: DayCellContentArg){
                    e.dayNumberText = e.dayNumberText.replace('日', '');
                },
                events: this.getHoliday(holidaysDate),
                eventContent: function(arg: EventContentArg){
                    document.querySelectorAll<HTMLElement>('.fc-daygrid-day').forEach(el => {
                        if(el.dataset.date == arg.event.extendedProps.holiday){
                            // classを一旦退避
                            let classes = el.getAttribute('class');
                            // holidayを追加してclass設定
                            el.setAttribute('class', classes as string + ' holiday');
                        }
                    });
                },
            } as object,
            holidaysDate: holidaysDate,
            lastDay: '',
        }
    },
    computed: {
        checkDate(){
            // 月が変わったら(日付が前回より小さくなったら)カレンダーリフレッシュ
            if(this.datetime['date'] < this.lastDay){
                (this.$refs.calendar as InstanceType<typeof FullCalendar>).$emit('refetch-events');
            }
            this.updateDate(this.datetime['date']);
            return this.datetime;
        }
    },
    methods: {
        getHoliday(holidaysDate: {[index: string]: string}){
            let events = [];
            let holidays: string[] = Object.keys(holidaysDate);
            for(let i = 0; i < holidays.length; i++){
                let holiday = {
                    title: holidaysDate[holidays[i]],
                    start: holidays[i],
                    className: 'holiday',
                    holiday: holidays[i],
                };
                events.push(holiday);
            }
            return events;
        },
        updateDate(dateNow: string){
            this.lastDay = dateNow;
        }
    }
});
</script>

<style lang="scss">
.monthly-calendar{
    width: calc(50% - 25px);
    &__date{
        display: none;
    }
    @media screen and (max-width: 768px){
        width: 100%;
    }
}
/* カレンダーのゾーン */
.fc .fc-toolbar.fc-header-toolbar{
    margin-bottom: 10px;
}
.fc-scrollgrid{
    background-color: #fff;
}
.fc-daygrid-day{
    background: #eee;
}
.fc-theme-standard td{
    border: 1px solid #fff;
}
.fc-col-header-cell-cushion,
.fc-daygrid-day-number{
    color: #333;
}
.fc-day-sat{
    background-color: #eaf4ff;
}
.fc-day-sat .fc-col-header-cell-cushion,
.fc-day-sat .fc-daygrid-day-number{
    color: #00f;
}
.fc-day-sun .fc-col-header-cell-cushion,
.fc-day-sun .fc-daygrid-day-number,
.holiday .fc-daygrid-day-number{
    color: #f00;
}
.fc-day-sun,
.holiday{
    background-color: #ffeaea;
}
.fc-col-header-cell{
    background-color: lightgray;
}
.fc-event-title{
    width: 100%;
    background: #DC143C;
    font-size: .9em;
    font-weight: bold;
    text-align: center;
}
.holiday.fc-h-event{
    border: 1px solid #DC143C;
}
</style>
