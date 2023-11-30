/**
 * Variables
 */

const chatRoom = document.querySelector('#room_uuid').textContent.replaceAll('"', '') // get room_uuid from room.html at block scripts and remove ""

let chatSocket = null

const userName = document.querySelector('#user_name').textContent.replaceAll('"', '')

const userId = document.querySelector('#user_id').textContent.replaceAll('"', '')


/**
 * Elements // We access all of these from room.html. because we define main_admin.js in that file
 */

const chatLogElement = document.querySelector('#chat_log')
const chatInputElement = document.querySelector('#chat_message_input')
const chatSubmitElement = document.querySelector('#chat_message_submit')


/**
 * Functions
 */


function scrollToBottom() {
    chatLogElement.scrollTop = chatLogElement.scrollHeight
}


function sendMessage() {
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': chatInputElement.value,
        'name': userName,
        'agent': userId,
    }))

    chatInputElement.value = ''
}


function onChatMessage(data) {
    console.log('onChatMessage', data)

    if (data.type == 'chat_message') {
        let tmpInfo = document.querySelector('.tmp-info')

        if (tmpInfo) {
            tmpInfo.remove()
        }

        if (!data.agent) {
            chatLogElement.innerHTML += `
            <div class="flex w-full mt-2 space-x-3 max-w-md">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>

                <div>
                    <div class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                        <p class="text-sm">${data.message}</p>
                    </div>
                    
                    <span class="text-xs text-gray-500 leading-none">${data.created_at} ago</span>
                </div>
            </div>
        `
        } else {
            chatLogElement.innerHTML += `
            <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                <div>
                    <div class="bg-blue-300 p-3 rounded-l-lg rounded-br-lg">
                        <p class="text-sm">${data.message}</p>
                    </div>
                    
                    <span class="text-xs text-gray-500 leading-none">${data.created_at} ago</span>
                </div>

                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>
            </div>
        `
        }
    } else if (data.type == 'writing_active') {
        if (!data.agent) {
            let tmpInfo = document.querySelector('.tmp-info')

            if (tmpInfo) {
                tmpInfo.remove()
            }

            chatLogElement.innerHTML += `
            <div class="tmp-info flex w-full mt-2 space-x-3 max-w-md">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300 text-center pt-2">${data.initials}</div>

                <div>
                    <div class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg">
                        <p class="text-sm">Client is writing a message...</p>
                    </div>
                </div>
            </div>
        `
        }
    }

    scrollToBottom()
}


/**
 * WebSocket
 */

chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${chatRoom}/`)

chatSocket.onmessage = function(e) {
    console.log('onMessage')

    onChatMessage(JSON.parse(e.data))
}

chatSocket.onopen = function(e) {
    console.log('onOpen')

    scrollToBottom()
}

chatSocket.onclose = function(e) {
    console.log('Chat socket closed unexpectadly')
}


/**
 * Event listeners
 */

chatSubmitElement.onclick = function(e) {
    e.preventDefault()

    sendMessage()

    return false
}

// Sned message by Enter
chatInputElement.onkeyup = function(e) {
    if (e.keyCode == 13) {
        sendMessage()
    }
}

chatInputElement.onfocus = function(e) {
    chatSocket.send(JSON.stringify({
        'type': 'update',
        'message': 'writing_active',
        'name': userName,
        'agent': userId,
    }))
}