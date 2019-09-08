function showImg(a){
    var imgUrl = $(a).attr("img-url");
    var note = $(a).attr("note");
    if(imgUrl == ""){
        return;
    }
    document.getElementById("img-modal").setAttribute('src', imgUrl);
    document.getElementById("note-modal").innerHTML = note;
}

