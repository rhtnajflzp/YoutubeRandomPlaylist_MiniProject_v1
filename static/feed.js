$(document).ready(function () {
    $('#__header__').load('/header');
    $('#__modal__').load('/modal');
});

function playlist(playlistId, userId) {
    location.href = "/randomplaylist?playlistId=" + playlistId + "&author=" + userId;
}

function tag_insert() {
    let tag = $('#tag-content').val();

    $.ajax({
        type: "POST",
        url: "/tag/insert",
        data: {
            'tag_give': tag
        },
        success: function (response) { // 성공하면
            window.location.reload();
        }
    })
}

function search_list(query) {
    location.href = '/randomplaylist?q=' + query;
}