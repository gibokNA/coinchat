<script setup lang="ts">
import { useMobileDetection } from 'vue3-mobile-detection'
import { use_global_store } from '@/stores/global_store'
import { use_websocket_store } from '@/stores/websocket_store'
import { storeToRefs } from 'pinia'

import { onMounted } from 'vue'

import Chart from './Main_Sub_Component/Chart.vue'
import Change_Rate_Per_Time from './Main_Sub_Component/Change_Rate_Per_Time.vue'
import Rapid_Change from './Main_Sub_Component/Rapid_Change.vue'
import Trade_Checker from './Main_Sub_Component/Trade_Checker.vue'

const global_store = use_global_store()
const websocket_store = use_websocket_store()

const {
  is_chart_button_clicked,
  is_change_rate_per_time_button_clicked,
  is_rapid_change_button_clicked,
  is_live_trade_button_clicked,
  main_page_container_height,
  is_mobile
} = storeToRefs(global_store)

const {
  is_websocket_connection_failed
} = storeToRefs(websocket_store)

let main_page_container: any

onMounted(() => {
  main_page_container = document.getElementById("main-page-container");

  var ro = new ResizeObserver(onResize)
  ro.observe(main_page_container)
})

function onResize() {
  if (is_mobile.value == true) {
    main_page_container_height.value = main_page_container.offsetHeight
  }
}


</script>

<template>
  <BContainer fluid="true"  id="main-page-container">
    <BRow v-if="is_chart_button_clicked">
      <BCol>
        <Chart></Chart>
      </BCol>
    </BRow>

    <BRow style="color: black; margin-top: 12px; margin-bottom: 12px;" v-if="is_mobile==false">
      <BCol style="padding-right: 6px;" cols="4" v-if="is_change_rate_per_time_button_clicked==true">
        <Change_Rate_Per_Time></Change_Rate_Per_Time>
      </BCol>

      <BCol style="padding: 0 6px;" cols="4" v-if="is_rapid_change_button_clicked==true">
        <Rapid_Change></Rapid_Change>
      </BCol>

      <BCol style="padding-left: 6px;" cols="4" v-if="is_live_trade_button_clicked==true">
        <Trade_Checker></Trade_Checker>
      </BCol>
    </BRow>

    <BRow v-else style="margin-bottom: 10px;">
      <BCol>
        <BRow v-if="is_change_rate_per_time_button_clicked==true" style="margin-top: 12px;"><BCol><Change_Rate_Per_Time></Change_Rate_Per_Time></BCol></BRow>

        <BRow v-if="is_rapid_change_button_clicked==true" style="margin-top: 12px;"><BCol><Rapid_Change></Rapid_Change></BCol></BRow>

        <BRow v-if="is_live_trade_button_clicked==true" style="margin-top: 12px;"><BCol><Trade_Checker></Trade_Checker></BCol></BRow>
      </BCol>
    </BRow>

    <BModal v-model="is_websocket_connection_failed" title="웹소켓 연결 안됨"> 새로고침 하거나, 계속 연결 안되면 나중에 다시 시도해주세요. </BModal>

  </BContainer>
</template>
