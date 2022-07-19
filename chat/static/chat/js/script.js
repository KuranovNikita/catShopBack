console.log('Работает скрипт файл')
var btnGet = document.querySelector('.chat_widget_btn_get');
btnGet.addEventListener("click", getText);
var btn = document.querySelector('.chat_widget_btn');
btn.addEventListener("click", getMessageFromTextarea);
document.querySelector('.chat_widget_textarea').addEventListener("keypress", submitOnEnter);

function submitOnEnter(event){
  if(event.which === 13 && !event.shiftKey){
    getMessageFromTextarea()
    event.preventDefault();
  }
}

function getText(){
  messages = sendName()
  console.log(messages)
  }

function makeMessages(messages) {
  console.log(messages)
  let dialog = document.querySelector('.chat_widget_messages');
  for (let i = 0; i < messages.length; i++) { 
    let div = document.createElement('div');
    div.className = "chat_widget_messages_element";
    div.textContent = messages[i]
    if (text !=''){
    dialog.append(div)
    }
  }
}


  async function sendName(){
    let data = {
        operatorName: "adminNik"
      }; 
    urlSendText = '/getDialogs'
    let messages = []
    let response = await fetch(urlSendText, {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json;charset=utf-8'
       },
       body: JSON.stringify(data)
     })
        .then(function(data) {
            data.json().then((json) => {
                console.log('внутре then' + json)
                messages = json.messages
                console.log('внутре then2' + messages)
                makeMessages(messages)
                })
        })
    console.log('внутре async' + messages)

return messages 
 }


function getMessageFromTextarea(){
  let textarea = document.querySelector('.chat_widget_textarea');
  text = textarea.value;
  console.log(typeof text)
  text = text.toString()
  console.log(typeof text)
  textarea.value = ''
  console.log(text);
  textarea.placeholder = "Введите текст...";
  sendMessage(text)
}



async function sendMessage(text){
  urlSendMessage = '/getMessageFromOperator'
  let data = {
    msg: text,
    userName: 'Telegram_Nikita_Kuranov_1246725945',
  };
  body = JSON.stringify(data)
  console.log(body)
  
 let response = await fetch(urlSendMessage, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: body
  })
  .then(function(response) {
    console.log(response)
  })
  .then(response => console.log(response));
}


