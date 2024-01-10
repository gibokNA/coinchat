<script setup lang="ts">

import { useMobileDetection } from 'vue3-mobile-detection'
import { use_global_store } from '@/stores/global_store'
import { use_websocket_store } from '@/stores/websocket_store'
import { storeToRefs } from 'pinia'

import { ref, computed, onMounted, onBeforeUnmount, inject } from 'vue'

const global_store = use_global_store()
const websocket_store = use_websocket_store()

const {
    main_page_container_height,
    is_mobile
} = storeToRefs(global_store)

const {
  message_list
} = storeToRefs(websocket_store)

const eventBus: any = inject('eventBus')

const message_list_group_height = ref(window.innerHeight - 205)

let variant_list = ["","primary","secondary","success","danger","warning","info","light","dark"]

let is_scroll_moved = false
const message_list_group_margin_right = ref("")

const top_height = computed(() => main_page_container_height.value)






let message_list_group: any

onMounted(() => {
  window.addEventListener('resize', onResize)

  message_list_group = document.getElementById("message-list-group")
  message_list_group!.addEventListener('scroll', handleScroll)

  if (is_mobile.value == true) {
    message_list_group_height.value = window.innerHeight - 265
  }
})

eventBus.on('message_recieved', move_scroll)

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
  message_list_group!.removeEventListener('scroll', handleScroll)
  eventBus.off('message_recieved', move_scroll)
})







function onResize() {
    if (is_mobile.value == false) {
      message_list_group_height.value = window.innerHeight - 205
    } else {
      message_list_group_height.value = window.innerHeight - 265

    if (is_scroll_moved === false) {
        setTimeout(move_scroll, 300)
    }
    }
}

function move_scroll() {
    if (is_scroll_moved === false) {
    if (message_list_group.scrollHeight > 0) {
        message_list_group.scrollTop = message_list_group.scrollHeight;
    }
    }
}

function handleScroll(event: any) {
    

    if (event.target.scrollTop + 5 >= (event.target.scrollHeight - message_list_group_height.value)) {
    is_scroll_moved = false
    message_list_group_margin_right.value = "margin-right: -20px;"
    } else {
    is_scroll_moved = true
    message_list_group_margin_right.value = ""
    }
}

function set_container_style() {
    if (is_mobile.value === true) {
      return 'position: absolute;top: ' + String(top_height.value) + 'px;right: 0;left: 0;outline: solid #2C333C 1px;background-color: #2F9D27;height: ' + String(window.innerHeight - 220) + 'px;'
    } else {
      return 'position: fixed;top: 0;right: 0;bottom: 0;width: 380px;outline: solid #2C333C 1px;background-color: #2F9D27;'
    }
}
    

</script>

<template>
  <BContainer fluid :style="set_container_style()">
    <BRow><BCol>
      <h5 style="margin-top: 10px;">채팅</h5>
    </BCol></BRow>
    <hr style="margin: 2px -10px 0px -10px;">
    <BRow>
      <BCol style="padding: 0px;">
        <BListGroup :style="'overflow-y: auto; height:' + String(message_list_group_height) + 'px;' + message_list_group_margin_right" id="message-list-group">
          <BListGroupItem v-for="data in message_list" :key="String(data['message_history_count'])+data['message']+data['nickname']" :variant="variant_list[data['message_history_count']%9]" style="padding: 0.5rem;">
            <span style="font-weight: bold; font-size:16px;">{{ data['nickname'] }}</span><span style="font-size:small;">{{ data['ip_address'] }}</span> {{ data['message'] }}
          </BListGroupItem>
        </BListGroup>
      </BCol>
    </BRow>
  </BContainer>
</template>
