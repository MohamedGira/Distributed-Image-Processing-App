tasks = [];
//get fastapi ws url
let url = window.location.origin;
let ws_url = url.replace("http://", "ws://");
const ws_root= ws_url.replace("https://", "ws://");


const start_smart_socket= (path)=>{
  const newSocket = new WebSocket(ws_root + path);
  console.log("smart socket created")
  newSocket.onmessage = async (event) => {
  const {topic, message} = JSON.parse(JSON.parse(event.data));
  await handle_result(newSocket,message);
  };
}


const handle_result = async (socket,data) => {
  if (data["status"] == "timeout") {
    handle_timeout(socket,data)
    status_text=document.getElementById(`${data["task_id"]}_status`).innerHTML = "timeout";
  }else if (data["status"] === "success") {
    const img = document.createElement("img");
    const response = await fetch(`/result?path=${data["output_means"]}`);
    const blob = await response.blob();
    let image = URL.createObjectURL(blob);
    img.src = image;
    img.className = "img-fluid";
    document.getElementById(`${data["task_id"]}_parent`).appendChild(img);
    tasks = tasks.filter((el) => el != data["task_id"]);
    status_text=document.getElementById(`${data["task_id"]}_status`).innerHTML = data["status"];
  }else{
    status_text=document.getElementById(`${data["task_id"]}_status`).innerHTML = data["status"];
  }
};

const handle_timeout = async (socket,data) => {
  //start another sokckt
  if (socket !== null && socket.readyState === WebSocket.OPEN) {
    socket.close();
  }
  start_smart_socket(`/result/${data.task_id}`);
}

