let container = document.getElementById("accordion");
let start_camera = document.querySelector("#start_camera");
let stop_camera = document.querySelector("#stop_camera");
let video = document.querySelector("#video");
let start_button = document.querySelector("#start-record");
let stop_button = document.querySelector("#stop-record");

let camera_stream = null;
let media_recorder = null;
let blobs_recorded = [];

start_camera.addEventListener("click", async function () {
  camera_stream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false,
  });
  video.srcObject = camera_stream;
});
start_button.addEventListener("click", function () {
  media_recorder = new MediaRecorder(camera_stream, { mimeType: "video/webm" });
  media_recorder.addEventListener("dataavailable", function (e) {
    blobs_recorded.push(e.data);
  });
  media_recorder.addEventListener("stop", function () {
    let video_local = URL.createObjectURL(
      new Blob(blobs_recorded, { type: "video/webm" })
    );
    console.log(video_local);
    let download_link = document.createElement("a");
    download_link.href = video_local;
    download_link.download = "Record.mp4";
    download_link.click();
  });
  media_recorder.start(1000);
});

stop_button.addEventListener("click", function () {
  media_recorder.stop();
  camera_stream.getTracks()[0].stop();
});

stop_camera.addEventListener("click", function () {
  camera_stream.getTracks()[0].stop();
});

function deletebtn(e) {
  let li = e.target.parentElement.parentElement.parentElement.parentElement;
  document.getElementById("delete-name").value =
    li.querySelector("a.name").innerText;
  container.removeChild(li);
  document.getElementById('submit-btn').click();
}
