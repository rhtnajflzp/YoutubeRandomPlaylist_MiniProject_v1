$(document).ready(function () {
    if (id != "") {
        // 로그인 정보 삽입
    }
});

function search_list(tag_name) {
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