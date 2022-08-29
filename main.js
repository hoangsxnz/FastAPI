let url = 'http://127.0.0.1:8000';

async function output() {
    let response = await fetch(url + '/ocr');
    let text = await response.text();
    return text; 
}

async function loadImage(event){
    var image = document.getElementById('output');
    image.src = URL.createObjectURL(event.target.files[0]);
}

async function uploadImg() {
    const formData  = new FormData();
    var image = document.getElementById('file').files[0];
    // console.log(image)
    formData.append("img", image)
    let res = await fetch(url + '/ocr/', {
        method: 'POST', 
        headers: {'Authorization': `Bearer ${localStorage.getItem("token")}`},
        // 'Content-Type': 'multipart/form-data',
        body: formData
    });

    if (res.ok) {
        let ret = await res.json();
        const {filename, text} = a;
        // window.location.href = url + download  // Redirect
        window.open(url + a);    // open newtab
    }
    else 
        console.log(`HTTP error: ${res.status}`)
}