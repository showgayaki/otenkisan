
<template>
    <div class="monthly-calendar">
        <FullCalendar ref="calendar" :options="calendarOptions()" />
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import '@fullcalendar/core/vdom';
import FullCalendar, { DayCellContentArg, EventContentArg } from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';

export default defineComponent({
    name: 'MonthlyCalendar',
    props: [
        'datetime',
        'holidaysDate',
    ],
    components: {
        FullCalendar,
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
        calendarOptions(){
            let options = {
                plugins: [ dayGridPlugin, interactionPlugin ],
                initialView: 'dayGridMonth',
                locale: 'ja',
                navLinks: false,
                fixedWeekCount: false,
                contentHeight: 'auto',
                dayCellContent: function(e: DayCellContentArg){
                    e.dayNumberText = e.dayNumberText.replace('日', '');
                },
                events: this.getHoliday(this.holidaysDate),
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
            }
            return options
        }
    }
});
</script>

<style lang="scss">
.monthly-calendar{
    width: 100%;
    &__date{
        display: none;
    }
    @media screen and (min-width: 576px){
        width: calc(50% - 15px);
    }
}
/* カレンダーのゾーン */
.fc .fc-toolbar-title,
.fc-toolbar-chunk{
    font-size: 14px;
}
.fc .fc-toolbar.fc-header-toolbar{
    margin-bottom: 5px;
}
.fc .fc-button{
    padding: 0 .65em;
}
.fc .fc-button .fc-icon{
    font-size: 1.2em;
}
.fc-scrollgrid{
    background-color: #fff;
}
.fc-daygrid-day{
    height: 2.4em;
    background: #eee;
}
.fc-theme-standard td{
    border: 1px solid #fff;
}
.fc-col-header-cell-cushion,
.fc .fc-daygrid-day-number{
    padding: 2px;
    color: #333;
    font-size: .7em;
}
.fc-day-sat{
    background-color: #eaf4ff;
}
.fc .fc-daygrid-body-unbalanced .fc-daygrid-day-events{
    min-height: unset;
}
.fc .fc-daygrid-body-natural .fc-daygrid-day-events{
    margin-bottom: 0;
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
.holiday.fc-h-event{
    border: none;
}
.fc-event-title{
    width: 100%;
    background: #DC143C;
    font-size: .6em;
    font-weight: bold;
    text-align: center;
    border: 1px solid #DC143C;
    border-radius: 3px;
}

@media screen and (min-width: 960px){
    .fc .fc-toolbar.fc-header-toolbar{
        margin-bottom: 10px;
    }
    .fc .fc-toolbar-title{
        font-size: 28px;
    }
    .fc .fc-button .fc-icon{
        font-size: 24px;
    }
    .fc-col-header-cell-cushion,
    .fc .fc-daygrid-day-number{
        font-size: 16px;
    }
    .fc-event-title{
        font-size: .8em;
    }
    .fc-daygrid-day{
        height: 2.7em;
        font-size: 18px;
    }
}
</style>
