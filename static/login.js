function sign_in() {
    let id = $("#input-id").val()
    let password = $("#input-password").val()

    //입력되지 않은 데이터 체크
    if (id == "") {
        $("#help-id-login").text("아이디를 입력해주세요.")
        $("#input-id").focus()
        return;
    } else {
        $("#help-id-login").text("")
    }

    if (password == "") {
        $("#help-password-login").text("비밀번호를 입력해주세요.")
        $("#input-password").focus()
        return;
    } else {
        $("#help-password-login").text("")
    }

    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            id_give: id,
            password_give: password
        },
        success: function (response) {
            if (response['result'] == 'success') {
                // 로그인 성공시 쿠키에 토큰 삽입.
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.replace("/")
            } else {
                alert(response['msg'])
            }
        }
    });
}