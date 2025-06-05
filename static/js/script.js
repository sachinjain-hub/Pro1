const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const output = document.getElementById('output');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
    setInterval(captureFrame, 100);
  });

function captureFrame() {
  const ctx = canvas.getContext('2d');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  canvas.toBlob(blob => {
    const formData = new FormData();
    formData.append('frame', blob);

    fetch('/process_frame', {
      method: 'POST',
      body: formData
    })
    .then(response => response.text())
    .then(data => {
      output.src = 'data:image/jpeg;base64,' + data;
    });
  }, 'image/jpeg');
}
