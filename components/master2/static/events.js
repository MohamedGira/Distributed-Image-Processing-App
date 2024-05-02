tasks = [];
//get fastapi ws url
let url = window.location.origin;
let ws_url = url.replace("http://", "ws://");
const ws_root= ws_url.replace("https://", "ws://");

const parse_message = (message) => {
  return JSON.parse(JSON.parse(message));
}

function handle_message(event_data) {
  const {topic, message} = parse_message(event_data);
  console.log(topic, message);
  if (topic == "result") {
    handle_result(message);
  }else if (topic == "timeout"){
    handle_timeout(message);
  }
}

const handle_result = async (data) => {
  if (data["status"] === "completed") {
    const img = document.createElement("img");
    const response = await fetch(`/result?path=${data["output_means"]}`);
    const blob = await response.blob();
    let image = URL.createObjectURL(blob);
    img.src = image;
    img.className = "img-fluid w-50";
    document.getElementById(`${data["task_id"]}_parent`).appendChild(img);
    tasks = tasks.filter((el) => el != data["task_id"]);
  } 
  status_text=document.getElementById(`${data["task_id"]}_status`).innerHTML = data["status"];
};

const handle_timeout = async (data) => {
  const socket = new WebSocket(ws_root + `/result/${data.task_id}`);
  socket.onmessage = (event) => {
    handle_message(event.data);
  };
}

