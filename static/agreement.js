$(function () {
    $("#accordion").accordion();
    $('#accordion input[type="checkbox"]').click(function (e) {
        e.stopPropagation();
    });
});

$.ajax({
    type: "GET",
    url: "/agreement",
    data: {},
    success: function (response) {
        window.location.replace("/sign_up")
    }
});