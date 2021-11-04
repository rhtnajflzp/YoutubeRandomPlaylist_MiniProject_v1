$(document).ready(function () {
    let parameters = get_query();
    let playlistId = parameters['playlistId'];

    if (playlistId) {
        play_playlist(playlistId);
    }

    let query = parameters['q'];
    if (query) {
        play_movie(query);
        $('#query').val(query);
        $('#comments').hide();
    }

    if (id != '') {
        //로그인 정보
        $('#__modal__').load("/modal.html");
    }
});

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

function search_list(id) {
    let query = $('#' + id).val();

    if (!query) {
        query = $('#' + id).text();
        query = query.substr(1);
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
            //console.log(response['list']);
            list.sort(() => Math.random() - 0.5);
            if (list && list.length > 0) {
                //console.log("총 영상 개수 : " + list.length);
                isPlay = true;
                nextVideo();

                $('#youtube-playlist').empty();
                $('#youtube-movie').show();
                $('#like').hide();
                $('#comments').hide();
            }
        }
    })
}

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

function nextVideo() {
    if (!isPlay) {
        return;
    }

    if (yt_idx >= list.length) {
    } else if (list[yt_idx]['id']['kind'] != 'youtube#video') {
        //console.log("Error! kind is not youtube#video. current kind : IDX " + yt_idx + " / "
        //    + list[yt_idx]['id']['kind']);
        while (++yt_idx < list.length && list[yt_idx]['id']['kind'] != 'youtube#video') {
            //    console.log("Error! kind is not youtube#video. current kind : IDX " + yt_idx + " / "
            //    + list[yt_idx]['id']['kind']);
        }
    } else if (list[yt_idx]['snippet']['liveBroadcastContent'] != 'none') {
        //console.log("Error! this is broadcast movie. current broadcast category : IDX " + yt_idx + " / "
        //        + list[yt_idx]['snippet']['liveBroadcastContent']);
        while (++yt_idx < list.length && list[yt_idx]['snippet']['liveBroadcastContent'] != 'none') {
            //    console.log("Error! this is broadcast movie. current broadcast category : IDX " + yt_idx + " / "
            //        + list[yt_idx]['snippet']['liveBroadcastContent']);
        }
    }

    //console.log("현재 idx : " + yt_idx);

    if (yt_idx >= list.length) {
        //console.log("영상 끝! 처음부터!");
        yt_idx = 0;
    }

    player.loadVideoById(list[yt_idx]['id']['videoId'], 0, "large");
    $('#author').text(list[yt_idx]['snippet']['channelTitle']);
    $('#title').text(list[yt_idx]['snippet']['title']);

    yt_idx++;
}

function play_playlist(id) {
    let temp_html = `<iframe id="youtube"
                width="690px" height="388px"
                src="https://www.youtube.com/embed/videoseries?list=${id}&autoplay=1&loop=1"
                title="YouTube video player" frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen></iframe>`;

    $('#youtube-movie').hide();
    $('#like').show();
    $('#comments').show();
    $('#youtube-playlist').empty();
    $('#youtube-playlist').append(temp_html);
}