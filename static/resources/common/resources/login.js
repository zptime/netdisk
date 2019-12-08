/**
 * Created by jie on 2016/8/29.
 */

$(function () {
    //记住密码
    $('#toggleBtn').click(function () {
        $(this).children('i').toggleClass('checkedBtn');
    });
    //记住密码
    var remember = Cookies.get('remember');
    if (remember == 'true') {
        var username = Cookies.get('username');
        var password = Cookies.get('password');
        // 自动填充帐号密码
        $('#username').val(username);
        $('#password').val(password);
        $('.checkBtn').addClass('checkedBtn')
    }
    $('.channel_item').on('click', function () {
        $(this).addClass('active').siblings().removeClass('active');
    });
});

$(function () {
    $('#login_btn').on('click', function () {
        //var data = $("#login_form").serialize();
        var url = '/user_center/api/login';
        $.ajax({
            url: url,
            data: {
                "username": $("#username").val(),
                "password": $("#password").val()
            },
            type: 'POST',
            success: function (data) {
                if (data.c != 0) {
                    $("#login_error").html(data.m)
                }
                else {
                    console.log(data);
                    if ($(".checkBtn").hasClass("checkedBtn")) {
                        var username = $("#username").val();
                        var password = $("#password").val();
                        // 设置cookie的有效期为14天
                        Cookies.set('username', username, {expires: 14});
                        Cookies.set('password', password, {expires: 14});
                        Cookies.set('remember', true, {expires: 14});
                    }
                    else {
                        // 删除cookie
                        Cookies.remove('username');
                        Cookies.remove('password');
                        Cookies.remove('remember');
                    }
                    //登录成功之后进入myhome聚合页
                    window.location.href = '/';
                }
            }
        })
    });
});
