<script setup lang="ts">
import { use_global_store } from '@/stores/global_store'
import { use_websocket_store } from '@/stores/websocket_store'
import { storeToRefs } from 'pinia'

const global_store = use_global_store()
const websocket_store = use_websocket_store()

const {
  selected_checker_version,
} = storeToRefs(global_store)

const {
  triggered_list
} = storeToRefs(websocket_store)

const { symbol_clicked, return_color } = global_store

function return_timestamp_to_hour_minute(timestamp: any) {
  var date = new Date(timestamp * 1000);

  var hours = String(date.getHours())
  if (hours.length === 1) {
    hours = '0' + hours
  }

  var minutes = String(date.getMinutes())
  if (minutes.length === 1) {
    minutes = '0' + minutes
  }

  return hours + ':' + minutes
}

</script>

<template>
    <BContainer fluid="true" style="padding: 0px;">
        <BRow>
            <BCol>
                <BCard no-body>
                    <BCardHeader>
                        <BRow align-h="between">
                        <BCol style="margin-top: 4px;" cols="auto">
                            실시간 급변동 종목
                        </BCol>
                        <BCol cols="auto">
                            <BRow>
                            <BCol style="padding: 0 6px;"><BButton @click="() => selected_checker_version = 'v1'" :variant="selected_checker_version=='v1'?'dark':'outline-dark'" size="sm" style="width: 50px;">1%</BButton></BCol>
                            <BCol style="padding: 0 6px;"><BButton @click="() => selected_checker_version = 'v2'" :variant="selected_checker_version=='v2'?'dark':'outline-dark'" size="sm" style="width: 50px;">2%</BButton></BCol>
                            <BCol style="padding: 0 6px;"><BButton @click="() => selected_checker_version = 'v3'" :variant="selected_checker_version=='v3'?'dark':'outline-dark'" size="sm" style="width: 50px;">3%</BButton></BCol>
                            </BRow>
                        </BCol>
                        </BRow>
                    </BCardHeader >

                    <BCardBody style="padding: 0px 11px;">
                      <BRow>
                        <BCol style="padding: 0px;">
                        <BListGroup id="live-change-rate-list-group">
                            <BListGroupItem v-for="data in triggered_list[selected_checker_version]" :key="data.triggered_time"
                            :style="'cursor: pointer; color: black; font-weight: bold; ' + return_color(data.change_rate, data.side)" @click="symbol_clicked(data.symbol)">
                            <BRow>
                                <BCol><BImg :src="'https://coinchat.work/icon/' + data.symbol.replace('/USDT','') + '.png'" style="width: 25px; margin-top: -5px;"></BImg> {{ data.symbol.replace("/","") }}</BCol>
                                <BCol>{{ data.side=="long"?'+':'-' }} {{ data.change_rate }} %</BCol>
                                <BCol cols="auto">{{ return_timestamp_to_hour_minute(data.triggered_time) }}</BCol>
                            </BRow>
                            </BListGroupItem>
                        </BListGroup>
                        </BCol>
                      </BRow>
                    </BCardBody>
                </BCard>
            </BCol>
        </BRow>
    </BContainer>
</template>
