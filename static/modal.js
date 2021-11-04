$(document).mouseup(function (e) {
    if ($('#modal').has(e.target).length === 0) {
        $('#modal_wrap').hide();
    }
});


function post_playlist() {
    let url = $('#modal-url').val();
    let title = $('#modal-title').val();

    let split_url = url.split('list=');
    let playlistId = split_url[split_url.length - 1].split('&');

    $.ajax({
        type: "POST",
        url: "/playlist/insert",
        data: {
            'playlistId_give': playlistId[0],
            'title_give': title
        },
        success: function (response) { // 성공하면
            alert(response['msg']);
            window.location.reload();
        }
    })
}

function modal_show() {
    $('#modal').show();
}