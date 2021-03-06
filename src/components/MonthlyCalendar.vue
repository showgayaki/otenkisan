
<template>
    <div class="monthly-calendar">
        <p class="monthly-calendar__date">{{ checkDate }}</p>
        <FullCalendar ref="calendar" :options="calendarOptions()" />
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import '@fullcalendar/core/vdom';
import FullCalendar, { DayCellContentArg, EventContentArg } from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import ApiService from '@/services/ApiService';
import ResponseData from '@/types/ResponseData';
import Holidays from '@/types/Holidays';

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
            holidaysDate: {} as Holidays,
            lastDay: '',
            refresh: false,
            loading: true,
            errored: false,
            errorText: '',
        }
    },
    mounted: function(){
        this.fetchHolidaysDate();
    },
    computed: {
        checkDate(){
            // 月が変わったら(日付が前回より小さくなったら)リフレッシュ
            if(Number(this.datetime['date']) < Number(this.lastDay)){
                // (this.$refs.calendar as InstanceType<typeof FullCalendar>).$emit('refetchEvents');
                location.reload();
            }
            this.updateDate(this.datetime['date']);
            return this.datetime;
        }
    },
    methods: {
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
