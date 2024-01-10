/* eslint-disable prefer-const */
import { ref, reactive, inject } from 'vue'
import { defineStore } from 'pinia'

export const use_websocket_store = defineStore('websocket_store', () => {

  const eventBus: any = inject('eventBus')

  const live_connections = ref(0)
  const triggered_list: {[key:string]: any} = reactive({'v1': [], 'v2': [], 'v3': []})
  const triggered_version = ref("v1")

  const trade_list = reactive({'value': [] as any[]})
  const change_rate_per_time_dict: {[key:string]: any} = reactive({'value': {}})

  const message_history_count = ref(0)
  const message_list: any[] = reactive([])

  const is_websocket_connection_failed = ref(false)
  
  const websocket = new WebSocket("wss://coinchat.work/ws/chat")

  websocket.onmessage = (event) => {

    let received_data = JSON.parse(event.data)
    let send_name = received_data['send_name']
    let data = received_data['data']
    let text_data

    if (send_name === "connect") {
      triggered_list["v1"] = data["triggered_list"]["v1"]
      triggered_list["v2"] = data["triggered_list"]["v2"]
      triggered_list["v3"] = data["triggered_list"]["v3"]


      for(let i of data["prev_message_list"]) {
          text_data = i
          text_data["message_history_count"] = message_history_count

          message_list.push(text_data)
          message_history_count.value += 1
      }

      change_rate_per_time_dict['value'] = data["change_rate_per_time_dict"]

      trade_list['value'] = data["trade_list"]

      setTimeout(() => eventBus.emit('message_recieved'), 200)

    } 
    else if (send_name === "chat_message") {
      if (message_list.length >= 200) {
          message_list.shift();
      }

      text_data = data["text_data"]
      text_data["message_history_count"] = message_history_count

      message_list.push(text_data)
      message_history_count.value += 1

      setTimeout(() => eventBus.emit('message_recieved'), 200)
    } 
    else if (send_name === "checker_triggered") {
      let triggered_data = data["triggered_data"]
      let version = data["version"]

      for (let [index, value] of triggered_list[version].entries()) {
        if (value['symbol'] === triggered_data['symbol']) {
          triggered_list[version].splice(index, 1)
        }
      }

      triggered_list[version].unshift(triggered_data)

      if (triggered_list[version].length > 10) {
        for (let i=0; i<triggered_list[version].length-10; i++) {
          triggered_list[version].pop()
        }
      }

      eventBus.emit("checker_triggered", data)

    } 
    else if (send_name === "get_live_connections") { live_connections.value = data["live_connections"] }
    else if (send_name === "get_change_rate_per_time_dict") {
      change_rate_per_time_dict['value'] = data["change_rate_per_time_dict"] 
      
      eventBus.emit('renewed_change_rate_per_time_dict')
    } 
    else if (send_name === "trade_checker") {
      trade_list['value'].unshift(data["trade_checker_data"])

      if (trade_list['value'].length > 10) {
        for (let i=0; i<trade_list['value'].length-10; i++) {
          trade_list['value'].pop()
        }
      }

      eventBus.emit("trade_checker", data)
    }
  }

  websocket.onopen = () => console.log("Successfully connected to the checker websocket server...")

  websocket.onclose = () => {
      console.log("websocket closed...")
      is_websocket_connection_failed.value = true
  }

  websocket.onerror = () => {
      console.log("websocket error...")
      is_websocket_connection_failed.value = true
  }

  return {
    live_connections,
    triggered_list,
    triggered_version,
    trade_list,
    change_rate_per_time_dict,
    websocket,
    message_history_count,
    message_list,
    is_websocket_connection_failed
  }
})
