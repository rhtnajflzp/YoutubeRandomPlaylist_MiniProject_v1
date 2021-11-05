$(document).mouseup(function (e) {
    // 영역 바깥 클릭시 포스팅박스가 숨겨지는 기능
    if ($('#modal').has(e.target).length === 0) {
        $('#modal_wrap').hide();
    }
});


function post_playlist() {
    let url = $('#modal-url').val();
    let title = $('#modal-title').val();

    /*  입력한 재생목록(변수 url)에서 필요한 정보인 playlistId만 분리하는 과정
     *  재생목록 예시
     *  https://www.youtube.com/watch?v=dPMktPKUOfg&list=PLguPqKADXoCEw_vJqW0VSNTKejjUAk2wY
     *  https://www.youtube.com/playlist?list=PLguPqKADXoCEw_vJqW0VSNTKejjUAk2wY
     *  https://www.youtube.com/embed/videoseries?list=PLguPqKADXoCEw_vJqW0VSNTKejjUAk2wY
     *  형식은 다양하지만, 어찌 되었든 playlist의 id는 list= 뒤에 담긴다.
     *  그러므로, list=로 한 번 자르고, 추가 파라미터가 존재할 가능성을 내포하지 않도록 &으로 한 번 더 자르고 0번 인덱스를 참조하면 playlistId만 담기게 된다.
     */

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