
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    var data = ev.target.id;
    ev.dataTransfer.setData("id", data);
}

function drop(ev) {
    ev.preventDefault();
    var src = $('#' + ev.dataTransfer.getData("id"));
    var tgt = $('#' + ev.target.id);

    // swap the contents of src and tgt
    var tmp = tgt.html();
    tgt.html(src.html());
    src.html(tmp);
}