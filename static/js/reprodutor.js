function cargarVideo() {
    let url = document.getElementById("youtubeUrl").value;

    let videoId = "";

    if (url.includes("watch?v=")) {
        videoId = url.split("watch?v=")[1].split("&")[0];
    }

    document.getElementById("videoFrame").src =
        `https://www.youtube.com/embed/${videoId}`;
}
