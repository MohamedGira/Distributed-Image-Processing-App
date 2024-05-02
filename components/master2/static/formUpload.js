async function submit_and_poll(id, formData) {
  const response = await fetch("/uploadOne", {
    method: "POST",
    body: formData,
  });
  //not clickable
  Toastify({
    text: "One Image Uploaded",
    duration: 3000,
    destination: null,
  }).showToast();
  const data = await response.json();

  if (data.task_id) {
    document.getElementById(`${id}_parent`).innerHTML = OutputContainer(
      data.task_id
    );
    const socket = new WebSocket(ws_root + `/result/${data.task_id}`);
    socket.onmessage = (event) => {
      handle_message(event.data);
    };
  }
}

async function submitForm(event) {
  event.preventDefault(); // Prevent the default form submission
  //upload in parallel
  requets = [];
  const formData = new FormData(event.target);
  let images = formData.getAll("images");
  process = formData.get("process");
  for (let i = 0; i < images.length; i++) {
    const image = images[i];
    const formData = new FormData();
    formData.append("image", image);
    formData.append("process", process);
    requets.push(submit_and_poll(i, formData));
  }
  let responses = await Promise.all(requets);
}