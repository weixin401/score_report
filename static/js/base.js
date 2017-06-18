/**
 * Created by root on 17-6-7.
 */
var loginDialog = new PSQDialog("login_dialog");
var registerDialog = new PSQDialog("register_dialog");

loginDialog.init(300,330);
registerDialog.init(300,390);

$('.login_button').click(function() {

    loginDialog.showDialog();
});
$('.register_button').click(function() {

    registerDialog.showDialog();
});

$('.login_userbutton').click(function()
{

    var _xsrf = getCookie("_xsrf");
    var username = $('.login_username input').val();
    var password = $('.login_password input').val();

    var data = {
        "username":username,
        "password":password,
        "_xsrf":_xsrf
    };
    $.post("/login",
        data,
        function(data,status){
            loginDialog.hideDialog();
        },
        "json"
    );

});
$('.register_userbutton').click(function()
{

    var _xsrf = getCookie("_xsrf");
    var username = $('.register_username input').val();
    var password = $('.register_password input').val();
    var repassword = $('.register_repeat input').val();

    var data = {
        "username":username,
        "password":password,
        "repassword":repassword,
        "_xsrf":_xsrf
    };
    $.post("/signup",
        data,
        function(data,status){
            if(status == "success")
            {
                registerDialog.hideDialog();
            }
            else
            {
                alert(data);
            }

        },
        "json"
    );

});

$(document).ready(function(){



});
$(window).scroll(function() {
    var p = $(window).scrollTop();
});

