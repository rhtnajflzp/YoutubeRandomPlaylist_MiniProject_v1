/* 슬픈 점은, 유튜브 영상에는 단일영상의 재생과 재생목록의 재생을 위한 플레이어가 별도로 존재한다는 점이다.
 * 그리고 Youtube Data API는 단일 영상 재생과 플레이리스트 재생을 혼용할 수 있도록 하는 기능을 지원하지 않는다는 것이다.
 * 두 개의 모드를 혼용하는 일이 거의 없기 때문이겠지. 하지만 우리는 이 기능이 반드시 필요했다.
 * 그래서 여러가지 해결방법 중, API 핸들링 중요도가 낮은 것을 iframe 태그로 불러오는 방법을 채택하기로 했다.
 * 이번 프로젝트에서는 단일영상에 대한 상세정보들을 얻어오는것이 중요했으므로 재생목록을 iframe으로 불러오기로 결정했다.
 */

$(document).ready(function () {
    $('#__header__').load("/header");
    let parameters = get_query();
    let playlistId = parameters['playlistId'];
    $('#comments').hide();

    // 파라미터에 playlistId가 있을 경우 플레이리스트 재생모드로
    if (playlistId) {
        play_playlist(playlistId);
        $('#like').show();
    }

    let query = parameters['q'];

    // 파라미터에 단일 영상에 대한 쿼리정보가 있을 경우 단일영상 재생모드로
    if (query) {
        setTimeout(() => {
            play_movie(query);
            $('#query').val(query);
        }, 1000);
    }

    if (id != '') {
        //로그인 정보
        $('#__modal__').load("/modal");
    }
});

// 유튜브 플레이어 예외처리
function onPlayerReady(event) {
    if (isPlay && list[yt_idx]['snippet']['liveBroadcastContent'] != 'none') {
        nextVideo();
    }
    event.target.playVideo();
}

function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.ENDED) {
        nextVideo();
    }
}

function onError(event) {
    console.log("에러났다!");
    yt_idx++;
    nextVideo();
}

// get 파라미터 수령해오는 함수
function get_query() {
    let url = document.location.href;
    let qs = url.substring(url.indexOf('?') + 1).split('&');
    let result = {}
    for (let i = 0; i < qs.length; i++) {
        qs[i] = qs[i].split('=');
        result[qs[i][0]] = decodeURIComponent(qs[i][1]);
    }
    return result;
}

function search_list(tag_name) {
    // 태그명으로 된 개체들을 가져와 그것을 그대로 검색어로 채용하는 방식을 사용했다.
    let query = $('#' + tag_name).val();

    if (!query) {
        query = $('#' + tag_name).text();
        query = query.split('#');
        if(query.length>0){
            query = query[query.length - 1];
        }else{
            query = query[0];
        }
        $('#query').empty();
        $('#query').val(query);
    }

    play_movie(query);
}

function play_movie(query) {
    $.ajax({
        type: "GET",
        url: "/search?q=" + query,
        data: {},
        success: function (response) { // 성공하면
            yt_idx = 0;
            //영상 정보 가져오기
            list = response['list']['items'];
            console.log(response['list']);
            list.sort(() => Math.random() - 0.5);
            if (list && list.length > 0) {
                //console.log("총 영상 개수 : " + list.length);
                isPlay = true;
                nextVideo();

                // 단일 영상 재생모드로 진입하기 위한 정리.
                $('#youtube-playlist').empty();
                $('#youtube-movie').show();
                $('#next-img').show();
                $('#like').hide();
                $('#comments').hide();
            }
        }
    })
}

function nextVideo() {
    // 단일 영상 재생 함수
    // 다음 영상을 재생시켜주는 index는 전역변수 yt_idx가 수행해준다.
    if (!isPlay) {
        return;
    }

    /*  유튜브 쿼리 결과에는 여러가지 종류가 있다.
     *  1. ['id']['kind'] : youtube#video(단일 영상), youtube#playlist(재생목록), youtube#channel(채널)
     *  2. ['snippet']['liveBroadcastContent'] : none(일반 영상), live(실시간 방송), upcoming(최초공개)
     *  이 중 youtube#video이면서 none인 것들만 재생하고자 했다.
     */
    if (yt_idx >= list.length) {
    } else if (list[yt_idx]['id']['kind'] != 'youtube#video') {
        // console.log("Error! kind is not youtube#video. current kind : IDX " + yt_idx + " / "
        //    + list[yt_idx]['id']['kind']);
        while (++yt_idx < list.length && list[yt_idx]['id']['kind'] != 'youtube#video') {
               // console.log("Error! kind is not youtube#video. current kind : IDX " + yt_idx + " / "
               // + list[yt_idx]['id']['kind']);
        }
    } else if (list[yt_idx]['snippet']['liveBroadcastContent'] != 'none') {
        // console.log("Error! this is broadcast movie. current broadcast category : IDX " + yt_idx + " / "
        //        + list[yt_idx]['snippet']['liveBroadcastContent']);
        while (++yt_idx < list.length && list[yt_idx]['snippet']['liveBroadcastContent'] != 'none') {
               // console.log("Error! this is broadcast movie. current broadcast category : IDX " + yt_idx + " / "
               //     + list[yt_idx]['snippet']['liveBroadcastContent']);
        }
    }

    // console.log("현재 idx : " + yt_idx);

    if (yt_idx >= list.length) {
        //console.log("영상 끝! 처음부터!");
        yt_idx = 0;
    }

    player.loadVideoById(list[yt_idx]['id']['videoId'], 0, "large");

    $('#author').text(list[yt_idx]['snippet']['channelTitle']);
    $('#title').text(list[yt_idx]['snippet']['title']);

    yt_idx++;
}

function play_playlist(playlistId) {
    // 재생목록 재생을 위한 함수
    // iframe에 url만 실어서 그대로 붙여넣는다.
    let temp_html = `<iframe id="youtube"
                width="951px" height="533px"
                src="https://www.youtube.com/embed/videoseries?list=${playlistId}&autoplay=1&loop=1"
                title="YouTube video player" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen></iframe>`;

    // 플레이리스트모드로 전환하기 위한 정리.
    $('#youtube-movie').hide();
    $('#next-img').hide();
    $('#like').show();
    $('#comments').show();
    $('#youtube-playlist').empty();
    $('#youtube-playlist').append(temp_html);

    set_playlist_info();
}

function set_playlist_info(){
    let parameters = get_query();
    let playlistId = parameters['playlistId'];
    let author = parameters['author'];

    $.ajax({
        type: "POST",
        url: "/playlist/search",
        data: {
            'author_give': author,
            'playlistId_give': playlistId
        },
        success: function (response) { // 성공하면
            let playlist = JSON.parse(response['playlist']);
            let nickname = JSON.parse(response['nickname']);

            $('#author').text(nickname['nickname']);
            $('#title').text(playlist['title']);
        }
    })
}

function insert_comment(){
    let comment = $('#comment').val();

    let parameters = get_query();
    let playlistId = parameters['playlistId'];
    let author  = parameters['author'];

    $.ajax({
        type: "POST",
        url: "/comment/insert",
        data: {
            'comment_give': comment,
            'playlistId_give': playlistId,
            'author_give': author
        },
        success: function (response) { // 성공하면
            window.location.reload();
        }
    })
}

function like_playlist(){
    // 플레이리스트 좋아요 추가/삭제를 위한 함수
    let parameters = get_query();
    let playlistId = parameters['playlistId'];
    let author = parameters['author'];

    $.ajax({
        type: "POST",
        url: "/likelist",
        data: {
            'author_give': author,
            'playlistId_give': playlistId
        },
        success: function (response) { // 성공하면
            console.log(response['msg']);
            window.location.reload();
        }
    })
}