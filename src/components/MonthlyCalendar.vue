
<template>
    <div class="monthly-calendar">
        <FullCalendar :options="calendarOptions" />
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import '@fullcalendar/core/vdom';
import FullCalendar, { DayCellContentArg, EventContentArg } from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import holidaysDate from '../assets/json/holiday.json';

export default defineComponent({
    name: 'MonthlyCalendar',
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
                            el.setAttribute('class', 'holiday');
                        }
                    });
                },
            },
            holidaysDate: holidaysDate,
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
        }
    }
});
</script>

<style lang="scss">
.monthly-calendar{
    width: calc(50% - 25px);
    @media screen and (max-width: 768px){
    }
}
/* カレンダーのゾーン */
.fc-scrollgrid{
    background-color: #fff;
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
.fc-day-sun .fc-daygrid-day-number{
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
.holiday .fc-h-event{
    border: 1px solid #DC143C;
}
</style>
