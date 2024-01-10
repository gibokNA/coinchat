<script setup lang="ts">
import { use_global_store } from '@/stores/global_store'
import { use_websocket_store } from '@/stores/websocket_store'
import { storeToRefs } from 'pinia'
import { ref, inject, onBeforeUnmount } from 'vue'

const eventBus: any = inject('eventBus')

const global_store = use_global_store()
const websocket_store = use_websocket_store()

const { symbol_clicked, return_color } = global_store

const {
  change_rate_per_time_dict
} = storeToRefs(websocket_store)

let change_rate_per_time_index = ref("6h")

function change_rate_per_time_index_button_clicked(index: string) {
  change_rate_per_time_index.value = index
}

const component_key = ref(0)

eventBus.on('renewed_change_rate_per_time_dict', renewed_change_rate_per_time_dict)
onBeforeUnmount(() => eventBus.off('renewed_change_rate_per_time_dict', renewed_change_rate_per_time_dict))

function renewed_change_rate_per_time_dict() {
    component_key.value += 1
}

</script>

<template>
    <BContainer fluid="true" style="padding: 0px;">
        <BRow>
            <BCol>
                <BCard no-body>
                    <BCardHeader>
                        <BRow>
                        <BCol>
                            <BRow>
                            <BCol style="padding: 0 3px 0 3px;">
                                <BButton style="width: 100%;" :variant="change_rate_per_time_index=='1h'?'danger':'outline-danger'" size="sm" @click="change_rate_per_time_index_button_clicked('1h')">1H</BButton>
                            </BCol>
                            <BCol style="padding: 0 3px;">
                                <BButton style="width: 100%;" :variant="change_rate_per_time_index=='3h'?'danger':'outline-danger'" size="sm" @click="change_rate_per_time_index_button_clicked('3h')">3H</BButton>
                            </BCol>
                            <BCol style="padding: 0 3px;">
                                <BButton style="width: 100%;" :variant="change_rate_per_time_index=='6h'?'success':'outline-success'" size="sm" @click="change_rate_per_time_index_button_clicked('6h')">6H</BButton>
                            </BCol>
                            <BCol style="padding: 0 3px;">
                                <BButton style="width: 100%;" :variant="change_rate_per_time_index=='12h'?'primary':'outline-primary'" size="sm" @click="change_rate_per_time_index_button_clicked('12h')">12H</BButton>
                            </BCol>
                            <BCol style="padding: 0 3px;">
                                <BButton style="width: 100%;" :variant="change_rate_per_time_index=='24h'?'primary':'outline-primary'" size="sm" @click="change_rate_per_time_index_button_clicked('24h')">24H</BButton>
                            </BCol>
                            </BRow>
                        </BCol>
                        </BRow>
                    </BCardHeader>

                    <BCardBody style="padding: 0px 11px;">
                        <BRow>
                            <BCol style="padding: 0px;">
                            <BListGroup id="live-change-rate-list-group" :key="component_key">
                                <BListGroupItem v-for="data in change_rate_per_time_dict['value'][change_rate_per_time_index]" :key="data.symbol"
                                :style="'cursor: pointer; color: black; font-weight: bold; ' + return_color(data.change_rate, data.side)" @click="symbol_clicked(data.symbol)">
                                <BRow>
                                    <BCol><BImg :src="'https://coinchat.work/icon/' + data.symbol.replace('/USDT','') + '.png'" style="width: 25px; margin-top: -5px;"></BImg> {{ data.symbol.replace("/","") }}</BCol>
                                    <BCol>{{ data.side=="long"?'+':'-' }} {{ data.change_rate }} %</BCol>
                                    <BCol cols="auto">{{ data.index }}.</BCol>
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
