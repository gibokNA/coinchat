<script setup lang="ts">
import { use_global_store } from '@/stores/global_store'
import { use_websocket_store } from '@/stores/websocket_store'
import { storeToRefs } from 'pinia'

const global_store = use_global_store()
const websocket_store = use_websocket_store()

const {
  trade_list,
} = storeToRefs(websocket_store)

const { symbol_clicked } = global_store

function return_color2(won: string, side: string) {
  if (side === "long") {
    if (Number(won.replace("억","")) >= 15) {
      return 'background: rgb(34,193,195); background: linear-gradient(0deg, rgba(34,193,195,1) 0%, rgba(157,253,45,1) 100%);'
    } else if (Number(won.replace("억","")) >= 10) {
      return 'background-color: #86E57F;'
    } else {
      return 'background-color: #B7F0B1;'
    }
  } else {
    if (Number(won.replace("억","")) >= 15) {
      return 'background: rgb(230,34,34); background: linear-gradient(90deg, rgba(230,34,34,1) 0%, rgba(252,176,69,1) 100%);'
    } else if (Number(won.replace("억","")) >= 10) {
      return 'background-color: #F15F5F;'
    } else {
      return 'background-color: #FFA7A7;'
    }
  }
}

</script>

<template>
    <BContainer fluid="true" style="padding: 0px;">
        <BRow>
            <BCol>
                <BCard no-body>
                    <BCardHeader>
                        <BRow>
                        <BCol style="margin-top: 4px;">
                            실시간 고래 체결
                        </BCol>
                        </BRow>
                    </BCardHeader>

                    <BCardBody style="padding: 0px 11px;">
                      <BRow>
                        <BCol style="padding: 0px;">
                        <BListGroup id="live-change-rate-list-group">
                            <BListGroupItem v-for="data in trade_list['value']" :key="data.id" @click="symbol_clicked('BTCUSDT')"
                            :style="'cursor: pointer; color: black; font-weight: bold; ' + return_color2(data.won, data.side)">
                            <BRow align-h="between">
                                <BCol cols="auto">바이낸스 선물</BCol>
                                <BCol cols="auto">$ {{ Math.round(data.price) }}</BCol>
                                <BCol cols="auto">{{ data.side=='long'?'롱':'숏' }}</BCol>
                                <BCol cols="auto" style="min-width: 60px; text-align: end;">{{ data.won }}</BCol>
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
