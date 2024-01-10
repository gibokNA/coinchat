<script setup lang="ts">
import default_indicators from './indicators.json'
import symbol_list from './symbol_list.json'

import { useMobileDetection } from 'vue3-mobile-detection'
import { use_global_store } from '@/stores/global_store'
import { storeToRefs } from 'pinia'
import { ref, watch, reactive } from 'vue'

const global_store = use_global_store()

const {
  now_symbol,
  is_mobile
} = storeToRefs(global_store)

const { symbol_clicked } =  global_store

const now_interval = ref("1")

const mobile_now_interval_dropdown_text = ref("1분")

watch(now_interval, () => {
  if (now_interval.value == '1') mobile_now_interval_dropdown_text.value = "1분"
  else if (now_interval.value == '5') mobile_now_interval_dropdown_text.value = "5분"
  else if (now_interval.value == '15') mobile_now_interval_dropdown_text.value = "15분"
  else if (now_interval.value == '30') mobile_now_interval_dropdown_text.value = "30분"
  else if (now_interval.value == '60') mobile_now_interval_dropdown_text.value = "1시간"
  else if (now_interval.value == '120') mobile_now_interval_dropdown_text.value = "2시간"
  else if (now_interval.value == '240') mobile_now_interval_dropdown_text.value = "4시간"
  else if (now_interval.value == '1D') mobile_now_interval_dropdown_text.value = "1일"
  else if (now_interval.value == '1W') mobile_now_interval_dropdown_text.value = "1주"
  else if (now_interval.value == '1M') mobile_now_interval_dropdown_text.value = "1달"

  localStorage.setItem("now_interval", now_interval.value)
})

if (localStorage.getItem("now_symbol") != null) { now_symbol.value = localStorage.getItem("now_symbol")! }
if (localStorage.getItem("now_interval") != null) { now_interval.value = localStorage.getItem("now_interval")! }

let chart_height = JSON.parse(localStorage.getItem("chart_height")!)

if (chart_height == null) {
  localStorage.setItem("chart_height", JSON.stringify(574))
  chart_height = JSON.parse(localStorage.getItem("chart_height")!)
}

const is_tradingview_ready = ref(false)

setTimeout(() => {
  is_tradingview_ready.value = true
}, 1000);

const symbol_input_text = ref("")

const matched_symbol_list = reactive({'value': symbol_list})

const before_apply_chart_height = ref(574)

const indicators: {[key:string]: any} = reactive({'value': default_indicators})

if (JSON.parse(localStorage.getItem("indicators")!) == null) {localStorage.setItem("indicators", JSON.stringify(indicators['value']))} 
else {indicators['value'] = JSON.parse(localStorage.getItem("indicators")!)}

const before_apply_indicators = reactive({'value': [] as any})

const chart_script = ref('')


function short_cut_keydown(event: any) {
  if (event.which === 13) {
    // The key pressed was the enter key
    event.preventDefault();
  }

  if (event.key == "ArrowLeft") {
    short_cut_button_clicked("prev")
  } else if (event.key == "ArrowRight") {
    short_cut_button_clicked("next")
  }
}

function short_cut_button_clicked(direction: string) {
  let now_symbol_index = symbol_list.indexOf(now_symbol.value)

  let target_symbol: any

  if (direction == "prev") {
    target_symbol = symbol_list[now_symbol_index - 1]
  } else if (direction == "next") {
    target_symbol = symbol_list[now_symbol_index + 1]
  }

  symbol_clicked(target_symbol)
}

function individual_indicator_setting_button_clicked(alias: any) {
  for (var i=0; i<before_apply_indicators['value'].length;i++) {
    if (before_apply_indicators['value'][i]['alias'] == alias) {
      before_apply_indicators['value'][i]["is_setting_open"] = !before_apply_indicators['value'][i]["is_setting_open"]

      break
    }
  }
}

function chart_setting_reset_button_clicked() {
  before_apply_indicators['value'] = default_indicators
  before_apply_chart_height.value = 574
}

let is_chart_setting_modal_show = ref(false)

function chart_setting_apply_button_clicked() {
  for (let i=0; i<before_apply_indicators['value'].length;i++) {
    if (before_apply_indicators['value'][i]["inputs"] != false) {
      for (let j of before_apply_indicators['value'][i]["inputs"]["parameter_name_list"]) {
        if (before_apply_indicators['value'][i]["inputs"][j["en_parameter_name"] + "_available"] == null) {
          before_apply_indicators['value'][i]["inputs"]["parameters"][j["en_parameter_name"]] = Number(before_apply_indicators['value'][i]["inputs"]["parameters"][j["en_parameter_name"]])
        }
      }
    }
  }

  localStorage.setItem("chart_height", JSON.stringify(before_apply_chart_height.value)!)
  localStorage.setItem("indicators", JSON.stringify(before_apply_indicators['value'])!)

  chart_height = JSON.parse(localStorage.getItem("chart_height")!)
  indicators['value'] = JSON.parse(localStorage.getItem("indicators")!)


  is_chart_setting_modal_show.value = false
}

function indicator_option_clicked(alias: any) {
  for (var i=0; i<before_apply_indicators['value'].length;i++) {
    if (before_apply_indicators['value'][i]['alias'] === alias) {
      before_apply_indicators['value'][i]["is_show"] = !before_apply_indicators['value'][i]["is_show"]

      break
    }
  }
}

function chart_setting_button_clicked() {
  before_apply_chart_height.value = JSON.parse(localStorage.getItem("chart_height")!)
  before_apply_indicators['value'] = JSON.parse(localStorage.getItem("indicators")!)

  is_chart_setting_modal_show.value = true
}

function symbol_input_text_changed(event: any) {
  
  if (event.which === 13) {
    // The key pressed was the enter key
    event.preventDefault();
  }

  setTimeout(() => {
    matched_symbol_list['value'] = []

    for (var i of symbol_list) {
      if (i.indexOf(symbol_input_text.value.toUpperCase()) !== -1) {
        matched_symbol_list['value'].push(i)
      }
    }

    if (symbol_input_text.value === "") {
      matched_symbol_list['value'] = symbol_list
    }
  }, 100)
}

function complete_script_string(selected_symbol: string, selected_interval: string) {

var studies = []
var studies_overrides: {[key:string]: string} = {}

for (var i of indicators['value']) {
  if (i['is_show'] === true) {
    studies.push(i['alias'] + "@tv-basicstudies")

    if (i['inputs'] != false) {
      for (var j of i["inputs"]["parameter_name_list"]) {
        studies_overrides[String(i["en_name"] + "." + j["en_parameter_name"])] = i["inputs"]["parameters"][j["en_parameter_name"]]
      }
    }
  }
}

var script_string = `new TradingView.widget({"studies": ` + JSON.stringify(studies) + `, "studies_overrides": ` + JSON.stringify(studies_overrides) + ` , "autosize": true,"symbol": "BINANCE:`
script_string += selected_symbol.replace("USDT","")

if (is_mobile.value === false) {
  script_string += `USDTPERP","interval": "` + selected_interval + `","timezone": "Asia/Seoul","theme": "dark","style": "1","locale": "kr","toolbar_bg": "#f1f3f6","enable_publishing": false,`
  script_string += `"withdateranges": true,"hide_side_toolbar": false,"allow_symbol_change": true,"details": false,"show_popup_button": true,"popup_width": "1000",`
  script_string += `"popup_height": "650","container_id": "tradingview_5da35", "details": true});`
} else {
  script_string += `USDTPERP","interval": "` + selected_interval + `","timezone": "Asia/Seoul","theme": "dark","style": "1","locale": "kr","toolbar_bg": "#f1f3f6","enable_publishing": false,`
  script_string += `"withdateranges": true,"hide_side_toolbar": true,"allow_symbol_change": true,"details": false,"show_popup_button": false,"popup_width": "1000",`
  script_string += `"popup_height": "650","container_id": "tradingview_5da35"});`
}

chart_script.value = script_string

return script_string
}

function set_container_style() {
  if (is_mobile.value == false) return 'padding: 0px;'
  else return 'padding: 0px; margin-top: 60px;'
}

</script>

<template>
    <BContainer fluid="true" :style="set_container_style()">
        <BRow align-h="between">
            <BCol cols="auto">
                <BRow>
                    <BCol cols="auto" style="padding: 6px;">
                        <BDropdown :style="is_mobile == false?'width: 230px;':''" variant="success" size="lg" id="symbol_dropdown">
                        <template #button-content>
                            <BImg :src="'https://coinchat.work/icon/' + now_symbol.replace('USDT','') + '.png'" style="width: 25px; margin-top: -5px;"></BImg> {{ now_symbol }}
                        </template>

                        <BDropdownForm style="margin: -10px;" @click="(e: any) => e.stopPropagation()">
                            <BFormInput
                            id="dropdown_input"
                            placeholder="BTCUSDT"
                            v-model="symbol_input_text"
                            @keydown="symbol_input_text_changed"
                            autocomplete="off"
                            size="lg"
                            ></BFormInput>
                        </BDropdownForm>
                        <BDropdownDivider></BDropdownDivider>
                        <BDropdownGroup>
                            <BDropdownItem @click="symbol_clicked('BTCUSDT')"><BImg src="https://coinchat.work/icon/BTC.png" style="width: 25px;"></BImg> <span style="font-weight: bold;">BTCUSDT</span></BDropdownItem>
                            <BDropdownItem @click="symbol_clicked('ETHUSDT')"><BImg src="https://coinchat.work/icon/ETH.png" style="width: 25px;"></BImg> <span style="font-weight: bold;">ETHUSDT</span></BDropdownItem>
                            <BDropdownItem @click="symbol_clicked('XRPUSDT')"><BImg src="https://coinchat.work/icon/XRP.png" style="width: 25px;"></BImg> <span style="font-weight: bold;">XRPUSDT</span></BDropdownItem>
                        </BDropdownGroup>
                        <BDropdownDivider></BDropdownDivider>
                        <BDropdownGroup id="dropdown_group">
                            <BDropdownItem v-for="symbol in matched_symbol_list['value']" :key="symbol" @click="symbol_clicked(symbol)"><BImg :src="'https://coinchat.work/icon/' + symbol.replace('USDT','') + '.png'" style="width: 25px;"></BImg> {{ symbol }}</BDropdownItem>
                        </BDropdownGroup>
                        </BDropdown>
                    </BCol>
                    <BCol cols="auto">
                        <BButton size="lg" style="margin-top: 6px; margin-left: -10px;" variant="warning" @click="chart_setting_button_clicked()"><IBiGear /></BButton>
                    </BCol>
                    <BCol cols="auto" v-if="is_mobile == false">
                        <BButton size="lg" style="margin-top: 6px; margin-left: -17px;" @click="short_cut_button_clicked('prev')" @keydown="short_cut_keydown"><IBiArrowLeftCircleFill /></BButton>
                    </BCol>
                    <BCol cols="auto" v-if="is_mobile == false">
                        <BButton size="lg" style="margin-top: 6px; margin-left: -17px;" @click="short_cut_button_clicked('next')" @keydown="short_cut_keydown"><IBiArrowRightCircleFill /></BButton>
                    </BCol>
                </BRow>
            </BCol>

            <BCol cols="auto" v-if="is_mobile == false">
                <BRow style="margin-top: 12px;">
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='1'?'primary':'outline-primary'" @click="() => now_interval = '1'">1분</BButton></BCol>
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='5'?'primary':'outline-primary'" @click="() => now_interval = '5'">5분</BButton></BCol>
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='15'?'primary':'outline-primary'" @click="() => now_interval = '15'">15분</BButton></BCol>
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='30'?'primary':'outline-primary'" @click="() => now_interval = '30'">30분</BButton></BCol>
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='60'?'success':'outline-success'" @click="() => now_interval = '60'">1시간</BButton></BCol>
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='120'?'success':'outline-success'" @click="() => now_interval = '120'">2시간</BButton></BCol>
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='240'?'success':'outline-success'" @click="() => now_interval = '240'">4시간</BButton></BCol>
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='1D'?'info':'outline-info'" @click="() => now_interval = '1D'">1일</BButton></BCol>
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='1W'?'info':'outline-info'" @click="() => now_interval = '1W'">1주</BButton></BCol>
                <BCol cols="auto" style="padding: 0px; padding-right: 10px;"><BButton :variant="now_interval==='1M'?'info':'outline-info'" @click="() => now_interval = '1M'">1달</BButton></BCol>
                </BRow>
            </BCol>
            <BCol v-else cols="auto" style="padding-right: 6px;">
                <BDropdown :text="mobile_now_interval_dropdown_text" size="lg" style="margin-top: 6px;" variant="primary">
                <BDropdownItem @click="() => now_interval = '1'">1분</BDropdownItem>
                <BDropdownItem @click="() => now_interval = '5'">5분</BDropdownItem>
                <BDropdownItem @click="() => now_interval = '15'">15분</BDropdownItem>
                <BDropdownItem @click="() => now_interval = '30'">30분</BDropdownItem>
                <BDropdownItem @click="() => now_interval = '60'">1시간</BDropdownItem>
                <BDropdownItem @click="() => now_interval = '120'">2시간</BDropdownItem>
                <BDropdownItem @click="() => now_interval = '240'">4시간</BDropdownItem>
                <BDropdownItem @click="() => now_interval = '1D'">1일</BDropdownItem>
                <BDropdownItem @click="() => now_interval = '1W'">1주</BDropdownItem>
                <BDropdownItem @click="() => now_interval = '1M'">1달</BDropdownItem>
                </BDropdown>
            </BCol>
            <hr id="HrText">
            </BRow>

            <BRow><BCol style="padding: 0; margin-top: -17px;">
            <!-- TradingView Widget BEGIN -->
            <div class="tradingview-widget-container">
                <div id="tradingview_5da35" :style="'height: ' + chart_height + 'px;'"></div>
                <component :is="'script'" type="text/javascript" src="https://s3.tradingview.com/tv.js"/>
                <component v-if="is_tradingview_ready" :is="'script'" type="text/javascript" :key="chart_script">{{ complete_script_string(now_symbol, now_interval) }}</component>
            </div>
            <!-- TradingView Widget END -->
            </BCol></BRow>

        

        <BModal v-model="is_chart_setting_modal_show" title="차트 지표 설정" scrollable>
            <BRow>
                <BCol cols="auto" style="margin-top: 5px;">차트 높이(height) :</BCol>
                <BCol><BFormInput v-model="before_apply_chart_height" type="number"></BFormInput></BCol>
            </BRow>
            <hr>
            <BRow v-for="indicator in before_apply_indicators.value" :key="indicator.en_name" style="margin-top: 5px;">
                <BCol>
                <BRow>
                    <BCol :style="indicator.is_show===true?'padding-right: 6px;':''">
                    <BButton :variant="indicator.is_show===true?'primary':'outline-primary'" style="width: 100%;" @click="indicator_option_clicked(indicator.alias)">{{ indicator.en_name }} ({{ indicator.ko_name }})</BButton>
                    </BCol>
                    <BCol cols="auto" v-if="indicator.is_show===true" style="padding-left: 0;">
                    <BButton variant="warning" @click="individual_indicator_setting_button_clicked(indicator.alias)">
                        <IBiGear v-if="indicator.is_setting_open===false" />
                        <IBiChevronDoubleDown v-else />
                    </BButton>
                    </BCol>
                </BRow>
                <BRow v-if="indicator.is_setting_open===true && indicator.is_show===true" style="margin-top: 5px;">
                    <BCol>
                    <BCard v-if="indicator.inputs != false">
                        <BRow v-for="parameter_name in indicator.inputs.parameter_name_list" :key="parameter_name.en_parameter_name" style="margin-bottom: 10px;">
                        <BCol cols="auto" style="margin-top: 5px;">{{ parameter_name.ko_parameter_name }} : </BCol>
                        <BCol v-if="indicator.inputs[parameter_name.en_parameter_name+'_available'] == null">
                            <BFormInput type="number" v-model="indicator.inputs.parameters[parameter_name.en_parameter_name]"></BFormInput>
                        </BCol>
                        <BCol v-else>
                            <BFormSelect v-model="indicator.inputs.parameters[parameter_name.en_parameter_name]" :options="indicator.inputs[parameter_name.en_parameter_name+'_available']" style="width: 100%; height: 38px;"></BFormSelect>
                        </BCol>
                        </BRow>
                    </BCard>
                    <BCard v-else>
                        <BRow>
                        <BCol>변경할 수 있는 설정이 없음</BCol>
                        </BRow>
                    </BCard>
                    </BCol>
                </BRow>
                </BCol>
            </BRow>

            <template #footer>
                <BRow>
                <BCol cols="auto"><BButton variant="dark" @click="chart_setting_reset_button_clicked()">초기화</BButton></BCol>
                <BCol cols="auto"><BButton variant="danger" @click="(() => { is_chart_setting_modal_show = false })">취소</BButton></BCol>
                <BCol cols="auto"><BButton variant="success" @click="chart_setting_apply_button_clicked()">적용</BButton></BCol>
                </BRow>
            </template>
        </BModal>

    </BContainer>
</template>

<style scoped>

  #dropdown_group {
    max-height: 300px;
    overflow-y: auto;
  }
  #HrText {
    background-color: white;
    height: 1px;
  }
</style>