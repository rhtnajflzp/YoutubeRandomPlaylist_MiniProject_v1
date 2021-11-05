$(document).ready(function () {
    $('#__header__').load("/header");
    if (id != "") {
        // 로그인 정보 삽입
    }
});

function search_list(tag_name) {
    // 검색 기능 실행시 영상 재생 화면으로 넘겨줌.
    let query = $('#' + tag_name).val();

    if (!query) {
        query = $('#' + tag_name).text();
        query = query.split('#');
        if (query.length > 0) {
            query = query[query.length - 1];
        } else {
            query = query[0];
        }
    }
    window.location.href = '/randomplaylist?q=' + query;
}