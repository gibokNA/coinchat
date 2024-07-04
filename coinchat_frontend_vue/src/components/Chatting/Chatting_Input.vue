<script setup lang="ts">
import { useMobileDetection } from 'vue3-mobile-detection'
import { use_global_store } from '@/stores/global_store'
import { use_websocket_store } from '@/stores/websocket_store'
import { storeToRefs } from 'pinia'

import { ref, computed } from 'vue'

const global_store = use_global_store()
const websocket_store = use_websocket_store()

const {
    main_page_container_height,
    ip_address,
    is_mobile
} = storeToRefs(global_store)

const { websocket } = websocket_store

let nickname = ref("")
let textarea_message = ref("")

let top_height = computed(() => main_page_container_height.value + (window.innerHeight - 220))

let send_message_count = 0
let prev_time = new Date().getTime() / 1000;

const text_modal_title = ref("")
const text_modal_text = ref("")

const is_text_modal_show = ref(false)

function send_button_clicked() {
    let nickname_input: any = document.querySelector("#nickname-input")
    let message_textarea: any = document.querySelector("#message_textarea")

    if (nickname.value === "") {
      nickname_input!.focus()
      return
    }

    if (textarea_message.value === "") {
      message_textarea.focus()
      return
    }


    let now_time = new Date().getTime() / 1000;

    if (now_time - prev_time > 15) {
      send_message_count = 0
      prev_time = now_time
    }

    if (send_message_count >= 5) {
      text_modal_title.value = "도배금지 !!!!"
      text_modal_text.value = "좀 쉬면서 해라..."
      is_text_modal_show.value = true
    } 
    else {
      let data = {
        nickname: nickname.value,
        message: textarea_message.value,
        ip_address: ip_address.value
      }

      websocket.send(JSON.stringify(data))

      send_message_count += 1
    }
    
    textarea_message.value = ""
}

function textarea_changed(event: any) {
    if (event.which === 13) {
    // The key pressed was the enter key
    event.preventDefault();
    send_button_clicked()
    }
}


function set_container_style() {
    if (is_mobile.value === true) {
    return 'position: absolute;top: ' + String(top_height.value) + 'px; left: 0px;right: 0px;height: 160px;outline: solid #2C333C 1px;background-color: #242424;'
    } else {
    return 'position: fixed;width: 380px;height: 160px;outline: solid #2C333C 1px;bottom: 0px;right: 0px;background-color: #242424;'
    }
}



</script>

<template>
  <BContainer fluid :style="set_container_style()">
    <BRow style="margin-top: 10px;">
      <BCol style="padding: 0px 10px;"><BFormInput id="nickname-input" v-model="nickname" placeholder="닉네임"></BFormInput></BCol>
      <BCol style="padding: 0px 10px 0px 10px; margin-top: 5px; margin-left: 25px;"><div>{{ ip_address }}</div></BCol>
      <BCol style="padding: 0px; margin-right: -30px;"><BButton  variant="primary" @click="send_button_clicked">보내기</BButton></BCol>
    </BRow>
    <BRow style="margin-top: 5px;">
      <BCol style="padding: 0px 10px;">
        <BFormTextarea
          id="message_textarea"
          placeholder="도배 금지"
          @keydown="textarea_changed"
          v-model="textarea_message"
        ></BFormTextarea>
      </BCol>
    </BRow>

    <BModal v-model="is_text_modal_show" :title="text_modal_title">
      {{ text_modal_text }}
    </BModal>
  </BContainer>
</template>

<style scoped>
  #message_textarea {
    height: 97px;
  }
</style>
