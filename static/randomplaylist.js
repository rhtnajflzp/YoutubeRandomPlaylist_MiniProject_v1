$(document).ready(function () {
    $('#__header__').load("/header");
    let parameters = get_query();
    let playlistId = parameters['playlistId'];
    $('#comments').hide();

    if (playlistId) {
        play_playlist(playlistId);
        $('#like').show();
    }

    let query = parameters['q'];

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
    if (!isPlay) {
        return;
    }

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
    let temp_html = `<iframe id="youtube"
                width="951px" height="533px"
                src="https://www.youtube.com/embed/videoseries?list=${playlistId}&autoplay=1&loop=1"
                title="YouTube video player" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen></iframe>`;

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