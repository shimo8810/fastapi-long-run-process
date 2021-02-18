const btn = document.getElementById("btn");
const progress = document.getElementById("progress");
const progTxt = document.getElementById("progress-txt");
const resTxt = document.getElementById("result-txt");

async function poll(taskId) {
  const resp = await fetch(`http://localhost:8000/task/${taskId}`);
  const data = await resp.json();
  progress.value = data["progress"];
  progTxt.innerText = data["progress"] + " (%)";
  if (data["status"] == "SUCCEEDED") {
    progTxt.innerText = "SUCCEEDED";
    return data["uri"];
  } else {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    return await poll(taskId);
  }
}

btn.addEventListener("click", () => {
  fetch("http://localhost:8000/task", {
    method: "POST",
  })
    .then((resp) => resp.json())
    .then((data) => poll(data["task_id"]))
    .then((res) => fetch(`http://localhost:8000${res}`))
    .then((resp) => resp.json())
    .then((data) => {
      resTxt.innerText = data["result"];
    });
});
