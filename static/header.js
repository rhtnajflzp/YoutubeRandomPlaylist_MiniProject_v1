function feed(){
    location.href = '/feed';
}

function post(){
    $('#modal_wrap').show();
}

function login(){
    location.href = '/login';
}

function logout(){
    $.removeCookie('mytoken', {path: '/'});
    window.location.reload();
}