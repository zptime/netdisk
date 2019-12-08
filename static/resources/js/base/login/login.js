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
        var username = Cookies.get('yonghuming');
        var password = Cookies.get('mima');
        // 自动填充帐号密码
        $('#yonghuming').val(username);
        $('#mima').val(password);
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
                "username": $("#yonghuming").val(),
                "password": $("#mima").val()
            },
            type: 'POST',
            success: function (data) {
                if (data.c != 0) {
                    $("#login_error").html(data.m)
                }
                else {
                    console.log(data);
                    if ($(".checkBtn").hasClass("checkedBtn")) {
                        var username = $("#yonghuming").val();
                        var password = $("#mima").val();
                        // 设置cookie的有效期为14天
                        Cookies.set('yonghuming', username, {expires: 14});
                        Cookies.set('mima', password, {expires: 14});
                        Cookies.set('remember', true, {expires: 14});
                    }
                    else {
                        // 删除cookie
                        Cookies.remove('yonghuming');
                        Cookies.remove('mima');
                        Cookies.remove('remember');
                    }
                    //登录成功之后进入myhome聚合页
                    window.location.href = '/';
                }
            }
        })
    });
});
