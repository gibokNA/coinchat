<script setup lang="ts">
import { use_global_store } from '@/stores/global_store'
import { use_websocket_store } from '@/stores/websocket_store'
import { storeToRefs } from 'pinia'
import { ref, inject, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const eventBus: any = inject('eventBus')

const global_store = use_global_store()
const websocket_store = use_websocket_store()

const {
  is_chart_button_clicked,
  is_chatting_button_clicked,
  is_change_rate_per_time_button_clicked,
  is_rapid_change_button_clicked,
  is_live_trade_button_clicked,
  selected_checker_version,
} = storeToRefs(global_store)

const {
  live_connections
} = storeToRefs(websocket_store)

function site_icon_clicked() {
  let current_path = route.path

  if (current_path == '/') router.go(0)
  else router.push({path: '/'})
}

const is_checker_sound_on = ref(true)

if (localStorage.getItem('is_checker_sound_on') == null) {
  localStorage.setItem('is_checker_sound_on', JSON.stringify(is_checker_sound_on.value))
} else {
  is_checker_sound_on.value = JSON.parse(localStorage.getItem('is_checker_sound_on')!)
}

const is_trade_sound_on = ref(true)

if (localStorage.getItem('is_trade_sound_on') == null) {
  localStorage.setItem('is_trade_sound_on', JSON.stringify(is_trade_sound_on.value))
} else {
  is_trade_sound_on.value = JSON.parse(localStorage.getItem('is_trade_sound_on')!)
}

const checker_audio_volume = ref(0.3)
const trade_audio_volume = ref(0.5)

let checker_audio1_arr: any[] = []
let checker_audio2_arr: any[] = []

let trade_audio1_arr: any[] = []
let trade_audio2_arr: any[] = []

let now_checker_audio1_index = 0;
let now_checker_audio2_index = 0;

let now_trade_audio1_index = 0;
let now_trade_audio2_index = 0;

setTimeout(() => {
  let checker_audio1 = new Audio('https://coinchat.work/checker1.wav');
  checker_audio1.loop = false
  checker_audio1.volume = 0.3
  checker_audio1_arr.push(checker_audio1)

  let checker_audio2 = new Audio('https://coinchat.work/checker2.wav');
  checker_audio2.loop = false
  checker_audio2.volume = 0.3
  checker_audio2_arr.push(checker_audio2)

  let trade_audio1 = new Audio('https://coinchat.work/trade1.wav');
  trade_audio1.loop = false
  trade_audio1.volume = 0.5
  trade_audio1_arr.push(trade_audio1)

  let trade_audio2 = new Audio('https://coinchat.work/trade2.wav');
  trade_audio2.loop = false
  trade_audio2.volume = 0.5
  trade_audio2_arr.push(trade_audio2)

  setTimeout(() => {
    for (let i = 0; i < 9;i++) {
      let checker_audio1 = new Audio('https://coinchat.work/checker1.wav');
      checker_audio1.loop = false
      checker_audio1.volume = 0.3
      checker_audio1_arr.push(checker_audio1)

      let checker_audio2 = new Audio('https://coinchat.work/checker2.wav');
      checker_audio2.loop = false
      checker_audio2.volume = 0.3
      checker_audio2_arr.push(checker_audio2)

      let trade_audio1 = new Audio('https://coinchat.work/trade1.wav');
      trade_audio1.loop = false
      trade_audio1.volume = 0.5
      trade_audio1_arr.push(trade_audio1)

      let trade_audio2 = new Audio('https://coinchat.work/trade2.wav');
      trade_audio2.loop = false
      trade_audio2.volume = 0.5
      trade_audio2_arr.push(trade_audio2)
    }
  }, 1000)
}, 100)


eventBus.on('checker_triggered', checker_triggered)
onBeforeUnmount(() => eventBus.off('checker_triggered', checker_triggered))

function checker_triggered(eventbus_data: any) {
  if (is_checker_sound_on.value == true && is_rapid_change_button_clicked.value == true && eventbus_data['version'] == selected_checker_version.value) {
    if (eventbus_data['triggered_data']["change_rate"] >= 2) {
      checker_audio2_arr[now_checker_audio2_index].play()

      if (now_checker_audio2_index >= 9) { now_checker_audio2_index = 0 } 
      else { now_checker_audio2_index += 1 }
    } 
    else {
      checker_audio1_arr[now_checker_audio1_index].play()

      if (now_checker_audio1_index >= 9) { now_checker_audio1_index = 0 } 
      else { now_checker_audio1_index += 1 }
    }
  }
}

eventBus.on('trade_checker', trade_checker)
onBeforeUnmount(() => eventBus.off('trade_checker', trade_checker))

function trade_checker(eventbus_data: any) {
  if (is_trade_sound_on.value === true && is_live_trade_button_clicked.value === true) {
    if (Number(eventbus_data['trade_checker_data']["won"].replace("억","")) >= 15) {
      trade_audio2_arr[now_trade_audio2_index].play()

      if (now_trade_audio2_index >= 9) { now_trade_audio2_index = 0 }
      else { now_trade_audio2_index += 1 }
    } 
    else {
      trade_audio1_arr[now_trade_audio1_index].play()

      if (now_trade_audio1_index >= 9) { now_trade_audio1_index = 0 } 
      else { now_trade_audio1_index += 1 }
    }
  }
}

watch(checker_audio_volume, () => {
  for (let i=0; i<10; i++) {
    checker_audio1_arr[i].volume = checker_audio_volume.value
    checker_audio2_arr[i].volume = checker_audio_volume.value
  }
})

watch(trade_audio_volume, () => {
  for (let i=0; i<10; i++) {
    trade_audio1_arr[i].volume = trade_audio_volume.value
    trade_audio2_arr[i].volume = trade_audio_volume.value
  }
})

const is_sound_setting_modal_show = ref(false)

function sound_button_clicked(sound_type: string) {
  if (sound_type == 'checker') {
    is_checker_sound_on.value = !is_checker_sound_on.value
    localStorage.setItem('is_checker_sound_on', JSON.stringify(is_checker_sound_on.value))
  } else {
    is_trade_sound_on.value = !is_trade_sound_on.value
    localStorage.setItem('is_trade_sound_on', JSON.stringify(is_trade_sound_on.value))
  }
}

function leftbar_button_clicked(button_index: number) {
  if (button_index == 0) {is_chart_button_clicked.value = !is_chart_button_clicked.value} 
  else if (button_index == 1) {is_chatting_button_clicked.value = !is_chatting_button_clicked.value}
  else if (button_index === 2) {is_change_rate_per_time_button_clicked.value = !is_change_rate_per_time_button_clicked.value}
  else if (button_index === 3) {is_rapid_change_button_clicked.value = !is_rapid_change_button_clicked.value} 
  else if (button_index === 4) {is_live_trade_button_clicked.value = !is_live_trade_button_clicked.value}
}

</script>

<template>
  <BContainer fluid style="width: 200px;position: fixed;top: 0;left: 0;bottom: 0;outline: solid #2C333C 1px;background-color: #212121;">

    <BRow align-v="center" align-h="start">
      <BCol cols="auto" id="site_icon" @click="site_icon_clicked">
        <BRow align-v="center" align-h="center">
          <BCol cols="auto" style="padding: 0px"
            ><BImg src="https://coinchat.work/1.png" fluid style="margin-top: 5px; margin-left:10px;"></BImg
          ></BCol>
          <BCol cols="auto" style=""><h4 style="margin-top: 15px">코인챗</h4></BCol>
        </BRow>
      </BCol>
    </BRow>

    <hr id="HrText" />
    <BRow>
      <BCol>
        <BButton
          :variant="is_chart_button_clicked ? 'success' : 'outline-success'"
          style="width: 100%; margin-top: 10px"
          @click="leftbar_button_clicked(0)"><IBiBarChartFill /> 차트</BButton>
      </BCol>
    </BRow>

    <BRow>
      <BCol>
        <BButton
          :variant="is_chatting_button_clicked ? 'success' : 'outline-success'"
          style="width: 100%; margin-top: 10px"
          @click="leftbar_button_clicked(1)"><IBiChatDotsFill /> 채팅</BButton>
      </BCol>
    </BRow>

    <hr id="HrText" />
    
    <BRow
      ><BCol
        ><BButton
          :variant="is_change_rate_per_time_button_clicked ? 'warning' : 'outline-warning'"
          style="width: 100%; margin-top: 10px"
          @click="leftbar_button_clicked(2)"
          >시간별 변동률 순위</BButton
        ></BCol
      ></BRow
    >
    <BRow
      ><BCol
        ><BButton
          :variant="is_rapid_change_button_clicked ? 'danger' : 'outline-danger'"
          style="width: 100%; margin-top: 10px"
          @click="leftbar_button_clicked(3)"
          >실시간 급변동 종목</BButton
        ></BCol
      ></BRow
    >
    <BRow
      ><BCol
        ><BButton
          :variant="is_live_trade_button_clicked ? 'info' : 'outline-info'"
          style="width: 100%; margin-top: 10px"
          @click="leftbar_button_clicked(4)"
          >실시간 고래 체결</BButton
        ></BCol
      ></BRow
    >

    <hr id="HrText" />
    <BRow
      ><BCol
        ><BButton style="width: 100%" variant="warning" @click="() => is_sound_setting_modal_show = true"
          ><IBiBellFill /> 사운드 설정</BButton
        ></BCol
      ></BRow
    >

    <hr id="HrText" />

    <BRow>
      <BCol>
        <BCard style="color: black; font-size: small;">참고용으로만 사용하세요.<br/><br/>
          이 사이트는 1920x1080 에 텍스트 배율 100% 환경에서 개발했습니다.<br/><br/> <span style="font-weight: bold; color: red;">노트북이나 다른 해상도를 사용하는 경우 브라우저를 확대하거나 축소하세요.</span></BCard>
      </BCol>
    </BRow>

    <hr id="HrText" />

    <BRow>
      <BCol>
        <BCard style="color: black">
          <BRow align-h="center"><BCol cols="auto" style="font-weight: bold">실시간 {{ live_connections }} 명</BCol></BRow>
        </BCard>
      </BCol>
    </BRow>


    <BModal v-model="is_sound_setting_modal_show" title="사운드 설정">
      <BRow>
        <BCol style="padding-right: 7px"
          ><BButton
            style="width: 100%"
            :variant="is_checker_sound_on ? 'primary' : 'outline-primary'"
            @click="sound_button_clicked('checker')"
            >실시간 급변동 종목</BButton
          ></BCol
        >
        <BCol style="padding-left: 7px"
          ><BButton
            style="width: 100%"
            :variant="is_trade_sound_on ? 'primary' : 'outline-primary'"
            @click="sound_button_clicked('trade')"
            >실시간 고래 체결</BButton
          ></BCol
        >
      </BRow>
      <BRow>
        <BCol style="padding-right: 7px; margin-top: 5px"
          ><BFormInput
            v-model="checker_audio_volume"
            type="range"
            style="width: 100%"
            min="0"
            max="1"
            step="0.1"
          ></BFormInput>
        </BCol>
        <BCol style="padding-left: 7px; margin-top: 5px"
          ><BFormInput
            v-model="trade_audio_volume"
            type="range"
            style="width: 100%"
            min="0"
            max="1"
            step="0.1"
          ></BFormInput>
        </BCol>
      </BRow>
    </BModal>
  </BContainer>
</template>

<style lang="css" scoped>
#HrText {
  background-color: white;
  height: 1px;
}
</style>
