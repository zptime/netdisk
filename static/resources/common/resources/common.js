/**
 * Created by jie on 2016/11/30.
 */

;$.extend({
    hxComAccount: function (options) {
        var defaults = {
            USER_TYPE:{
                USER_TYPE_NOT_SET : 0,
                USER_TYPE_STUDENT : 1,
                USER_TYPE_TEACHER : 2,
                USER_TYPE_PARENT : 4
            },
            account: {}, //登录用戶
            rightTabReload: true, //默认刷新rightTab
            layer_textbook: {
                end: null  //layer_textbook关闭回调
            }
        };
        options = $.extend(options,defaults);

        //刷新组件
        function refresh(){
            setRightTabReload(true);
        }
        //设置刷新flag
        function setRightTabReload(flag){
            options.rightTabReload = !!flag;
        }

        //获取学校管理中心地址
        function getUserCenterUrl(){
            $.ajax({
                url: '/user_center/api/get/user_center_url',
                data: {},
                type: 'POST',
                error: function (data) {
                    console.log('请求超时');
                },
                success: function (data) {
                    if (data.c == 0) {
                        var val = data.d[0];
                        $('#USER_CENTER_URL').val(val);
                    } else {
                        console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                    }
                }
            });
        }

        //初始化用户信息
        function initAccount(){
            //获取用户个人信息
            $.ajax({
              url:  '/user_center/api/detail/account',
              data: {},
              type: 'POST',
              error: function (data) {
                 console.log('请求超时');
              },
              success: function (data) {
                 options.account = {};
                 if (data.c == 0) {
                    options.account = data.d[0];
                    setHeaderInfo();
                    loadleftInfo();
                 }else{
                    console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                 }
              }
            });
            //姓名 学校 + 角色 头像 个人信息
            function setHeaderInfo(){
                var obj = options.account;
                $("#current_school_id").val(obj.school_id);
                $("#current_type_id").val(obj.type_id);
                $('.hx-account-text-1').html(obj.full_name);
                $('.hx-account-text-2').html(obj.school_name+obj.type_name);
                if (obj.image_url){
                   $('.hx-account-img').attr('src',obj.image_url);
                }else{
                   $('.hx-account-img').attr('src',"/static/resources/common/resources/images/photo-default.png"); //默认头像
                };
            }
            //左侧公共个人信息
            function loadleftInfo(){
                var obj = options.account;
                $('.acc-box .photo').attr('src',obj.image_url?obj.image_url:'/static/resources/common/resources/images/photo-default.png');
                $('.acc-box .name-type').html(obj.full_name + '·' + obj.type_name);
                $('.acc-box .username.val').html(obj.username);
                $('.acc-box .viewPersonLink').on('click',function(){
                  window.location.href =  $('#USER_CENTER_URL').val() + '/person/index';
                });
                $('#hx-modal-account-exit').on('click',function() {
                    layer.confirm('确认退出系统?', {
                       icon: 3,
                       title: '提示',
                       btn:['确定','取消'],
                       yes: function (index) {
                           layer.close(index);
                           window.location.href = '/logout'
                       },
                       cancel: function(index){
                           layer.close(index);
                       }
                    });
                });
            };
        }

        //拿到登录用戶account
        function getAccount(milliseconds){
            var res = null;
            var waitTime = 5000 ; // 默认等待时间 5 秒
            if( typeof (milliseconds) == 'number'){
                waitTime = milliseconds;
            };
            if ( typeof(options.account.account_id)!='undefined' ){
                res = options.account;
            }else{
                //获取用户个人信息
                $.ajax({
                  url:  '/user_center/api/detail/account',
                  data: {},
                  type: 'POST',
                  async: false,
                  time: waitTime,
                  success: function (data) {
                     options.account = {};
                     if (data.c == 0) {
                        options.account = data.d[0];
                        res = options.account;
                     }
                  }
                });
            }
            if( res == null){
                layer.msg('请求超时,获取用户登录信息失败.');
            }
            return res;
        }

        //获取用户的类型code值
        function getTypeCodeById(id){
            var res = '';
            switch  (id){
                case '1':
                    res = 'student';
                    break;
                case '2':
                    res = 'teacher';
                    break;
                case '4':
                    res = 'parent';
                    break;
                default :
                    res = '';
            }
            return res;
        }

        //加载右侧tab-列表
        function loadrightTab(settings) {
            if( !options.rightTabReload ){//刷新flag关闭时
                return;
            };
            //准备加载rightTab数据
            (function(){
                /**bind**/
                $('.modal-account-right .box-1 .tab li').unbind().on('click', function () {
                    $('.modal-account-right .box-1 .tab li hr').remove();
                    $('.modal-account-right .box-1 .tab li a').removeClass('active');
                    $(this).append('<hr>');
                    $(this).children('a').addClass('active');
                    $('.modal-account-right .box-1 .content>div').css('display', 'none');
                    $('.modal-account-right .box-2>div').css('display', 'none');
                    var f = $(this).attr('role');
                    $('.modal-account-right .box-1 .content>div.' + f).css('display', 'block');
                    $('.modal-account-right .box-2>div.' + f).css('display', 'block');
                });
                var user_type = options.account.type_id;
                if (user_type == options.USER_TYPE.USER_TYPE_STUDENT) {
                    $('.modal-account-right [role="tab-class"]').remove();
                    $('.modal-account-right [role="tab-textbook"]').remove();
                    $('.modal-account-right [role="tab-identity"]').click();
                    initTabIdentity();
                } else if (user_type == options.USER_TYPE.USER_TYPE_TEACHER) {
                    $('.modal-account-right [role="tab-class"]').click();
                    initTabClass();
                    initTabIdentity();
                    initTextbook();
                } else if (user_type == options.USER_TYPE.USER_TYPE_PARENT) {
                    $('.modal-account-right [role="tab-class"]').remove();
                    $('.modal-account-right [role="tab-textbook"]').remove();
                    $('.modal-account-right [role="tab-identity"]').click();
                    initTabIdentity();
                };
                setRightTabReload(false); //关闭刷新flag
            })();
            //初始化班级（教师特有）
            function initTabClass() {
                //获取所授班级数据
                (function (){
                    $.ajax({
                        url: '/user_center/api/list/teacher_class',
                        type: 'POST',
                        dataType: 'json',
                        data: {},
                        error: function (data) {
                            console.log('请求超时');
                            layer.msg("请求超时");
                        },
                        success: function (data) {
                            if (data.c == 0) {
                                var class_list = data.d;
                                reset_class_ul( class_list );
                            } else {
                                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                                layer.msg('操作失败：' + data.m)
                            }
                        }
                    })
                })();

                //渲染班级列表
                function reset_class_ul(class_list){
                    var _html = '<div class="tab-content-h">';
                    if (class_list.length > 0) {
                        _html += '<ul>';
                        for (var i = 0; i < class_list.length; i++) {
                            var classObj = class_list[i];
                            _html +=
                                '<li class="tab-class-li">' +
                                '<span class="s-flag">' +
                                    '<img src="/static/resources/common/resources/images/class-default.png">' +
                                '</span>'+
                                '<span class="s-class">' + classObj.class_name + '</span>' +
                                '</li>'
                        }
                        _html += '</ul>';
                    }
                    _html += '</div>';
                    $('.modal-account-right .box-1 .content .tab-class').html(_html);
                    $(".modal-account-right .box-1 .content .tab-class .tab-content-h").mCustomScrollbar();
                }

                //管理我的班级
                $('.modal-account-right .box-2 .tab-class .btn').unbind().on('click', function () {
                    //关闭acc-modal-account
                    $('.hx-layer-account-container').attr("hidden", "hidden");
                    //打开管理班级
                    var layer_class = layer.open({
                        type: 1,
                        title: '授课班级管理',
                        area: ['880px', '480px'],
                        content: $('#acc-modal-class'),
                        btn: false,
                        end: function(){
                            $('.acc-modal-class .modal-3 .cancel-btn').click();
                            $('.acc-modal-class .modal-2 .cancel-btn').click();
                        }
                    });
                    window.layer_class = layer_class;
                    //初始化layer
                    init_acc_class();
                });
            };
            //初始化身份
            function initTabIdentity() {
                //获取身份数据
                (function () {
                    $.ajax({
                        url: '/user_center/api/list/user_type',
                        type: 'POST',
                        dataType: 'json',
                        data: {},
                        error: function (data) {
                            console.log('请求超时');
                            layer.msg("请求超时");
                        },
                        success: function (data) {
                            if (data.c == 0) {
                                var identity_list = data.d;
                                reset_identity_ul(identity_list);
                            } else {
                                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                                layer.msg('操作失败：' + data.m)
                            }
                        }
                    });
                })();

                //渲染身份列表
                function reset_identity_ul(identity_list) {
                    var _html = '<div class="tab-content-h">';
                    if (identity_list.length > 0) {
                        _html += '<ul>';
                        for (var i = 0; i < identity_list.length; i++) {
                            var identity = identity_list[i];
                            _html +=
                                '<li class="tab-identity-li">' +
                                '<span class="s-flag">'+
                                    ((identity.type_id == $('#current_type_id').val() && identity.school_id == $('#current_school_id').val())
                                    ? '<img src="/static/resources/common/resources/images/icon-active.png">':'') +
                                '</span>'+
                                '<span class="s-name">' + identity.full_name + '</span>' +
                                '<span class="s-type">' + identity.type_name + '</span>' +
                                '<span class="s-school">' + identity.school_name + '</span>' +
                                '</li>'
                        }
                        _html += '</ul>';
                    }
                    _html += '</div>';
                    $('.modal-account-right .box-1 .content .tab-identity').html(_html);
                    $(".modal-account-right .box-1 .content .tab-identity .tab-content-h").mCustomScrollbar();
                }

                //管理我的身份
                $('.modal-account-right .box-2 .tab-identity .btn').unbind().on('click', function () {
                    //关闭acc-modal-account
                    $('.hx-layer-account-container').attr("hidden", "hidden");
                    //打开用户角色选择
                    var layer_identity = layer.open({
                        type: 1,
                        title: '用户角色选择',
                        area: ['550px', '400px'],
                        content: $('#acc-modal-identity'),
                        btn: false
                    });
                    window.layer_identity = layer_identity;
                    //初始化layer
                    init_acc_identity();
                });
            };
            //初始化教材 (教师特有)
            function initTextbook() {
                //获取教材数据
                (function () {
                    $.ajax({
                        url: '/user_center/api/list/teacher_textbook',
                        type: 'POST',
                        dataType: 'json',
                        data: {},
                        error: function (data) {
                            console.log('请求超时');
                        },
                        success: function (data) {
                            if (data.c != 0) {
                                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                            } else {
                                var textbook_list = data.d;
                                reset_textbook_ul(textbook_list);
                            }
                        }
                    });
                })();

                //渲染教材列表
                function reset_textbook_ul(textbook_list) {
                    var _html = '<div class="tab-content-h">';
                    if (textbook_list.length > 0) {
                        _html += '<ul>';
                        for (var i = 0; i < textbook_list.length; i++) {
                            var textbook = textbook_list[i];
                            _html +=
                                '<li class="tab-textbook-li">' +
                                (textbook.is_current ? '<span class="s-flag">主</span>' : '<span class="s-flag f0"></span>') +
                                '<span class="s-subject">' + textbook.subject_name + '</span>' +
                                '<span class="s-name">' + textbook.textbook_name + '</span>' +
                                '</li>'
                        }
                        _html += '</ul>';
                    }
                    _html += '</div>';
                    $('.modal-account-right .box-1 .content .tab-textbook').html(_html);
                    $(".modal-account-right .box-1 .content .tab-textbook .tab-content-h").mCustomScrollbar();
                }

                //管理我的教材
                $('.modal-account-right .box-2 .tab-textbook .btn').unbind().on('click', function () {
                    //关闭acc-modal-account
                    $('.hx-layer-account-container').attr("hidden", "hidden");
                    //打开管理教材
                    var layer_textbook = layer.open({
                        type: 1,
                        title: '管理教材',
                        area: ['880px', '480px'],
                        content: $('#acc-modal-textbook'),
                        btn: false,
                        end: function () {
                            $('.acc-modal-textbook .modal-3 .cancel-btn').click();
                            $('.acc-modal-textbook .modal-2 .cancel-btn').click();
                            if ( settings && settings.layer_textbook && typeof (settings.layer_textbook.end)  == 'function'){
                                settings.layer_textbook.end.apply();
                            }
                        }
                    });
                    window.layer_textbook = layer_textbook;
                    //初始化layer
                    init_acc_textbook();
                });
            }
        };

        /*
        班级 ===================================================================================================================
        */
        function init_acc_class(){
            get_my_class_list();
            //获取我的授课班级 (授课班级管理)
            function get_my_class_list(){
                $.ajax({
                    url: '/user_center/api/list/teacher_class',
                    type: 'POST',
                    dataType: 'json',
                    data: {},
                    error: function(data) {
                        console.log('请求超时');
                    },
                    success: function(data) {
                        if (data.c != 0) {
                            console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                        }else{
                            var class_list = data.d;
                            reset_class_ul(class_list);
                            bindEvent();
                        }
                    }
                });
            }
            //渲染我的所授班级 （授课班级管理）
            function reset_class_ul(class_list){
                var _html = '';
                if (class_list.length > 0){
                    _html += '<ul>';
                    for(var i=0; i<class_list.length; i++){
                        var classObj = class_list[i];
                        _html +=
                            '<li>' +
                                '<div class="s-box">' +
                                    '<span class="s-subject">'+ '' +'</span>' +
                                    '<span class="s-name">'+ classObj.class_name +'</span>' +
                                    '<el class-id="'+ classObj.class_id +'" class-name="' + classObj.class_name + '" class="remove">×</el>'+
                                '</div>' +
                            '</li>';
                    }
                    _html += '</ul>';
                }
                $('.acc-modal-class .modal-1 .d-box').html(_html);
                $('.acc-modal-class .modal-1 .d-box').mCustomScrollbar();
            }
            //获取全校年级列表（添加所授班级）
            function get_all_grade_list(){
                var grade_list = null,defaults = [];
                $.ajax({
                    url: '/user_center/api/list/grade',
                    type: 'POST',
                    dataType: 'json',
                    error: function (data) {
                        console.log('请求超时');
                    },
                    success: function (data) {
                        if (data.c == 0)
                            grade_list = data.d
                        else
                            grade_list = defaults
                        reset_all_grade_list( grade_list );
                    }
                });
            }
            //获取全校班级列表（添加所授班级）
            function get_all_class_list(){
                $.ajax({
                    url: '/user_center/api/list/class',
                    type: 'POST',
                    data: {
                        teach_class: 1 //显示 当前用户所授班级标识
                    },
                    dataType: 'json',
                    error: function (data) {
                        console.log('请求超时');
                    },
                    success: function (data) {
                        var res = [];
                        if (data.c == 0){
                            var class_list = data.d;
                            reset_all_class_list (class_list);
                        }
                    }
                });
            }
            //渲染年级列表（添加所授班级）
            function reset_all_grade_list(grade_list){
                var _html = '';
                if (grade_list.length > 0){
                    _html += '<ul>';
                    for(var i=0; i<grade_list.length; i++){
                        var grade = grade_list[i];
                        _html +=
                            '<li role="filter_class" grade-num="'+ grade.grade_num +'">'+ grade.grade_name +'</li>'
                    }
                    _html += '</ul>';
                };
                $('.acc-modal-class .modal-2 .left-menu').html(_html);
                $('.acc-modal-class .modal-2 .left-menu').mCustomScrollbar();
                $('.acc-modal-class .modal-2 .left-menu [role="filter_class"]').unbind().on('click', function () {
                    var grade_num = $(this).attr('grade-num');
                    $('.acc-modal-class .modal-2 .right-class li').css('display','none');
                    $('.acc-modal-class .modal-2 .right-class li[grade-num="'+ grade_num +'"]').css('display','inline-block');
                    $('.acc-modal-class .modal-2 .left-menu [role="filter_class"]').removeClass('active');
                    $(this).addClass('active');
                });
            }
            //渲染班级列表（添加所授班级）
            function reset_all_class_list(class_list){
                var _html = '';
                if (class_list.length > 0){
                    _html += '<ul>';
                    for(var i=0; i<class_list.length; i++){
                        var classObj = class_list[i];
                        if (!classObj.is_teach){ // 未授课班级
                            _html +=
                                '<li role="choose_class" grade-num="'+ classObj.grade_num +'" class-id="' + classObj.id + '">' +
                                    '<div class="one-little-box">' +
                                        '<div class="div-box">' +
                                            '<img class="middle-img" src="/static/resources/common/resources/images/class-default.png">' +
                                            '<div class="middle-context">' +
                                                '<div class="class-name">' +
                                                    classObj.class_name +
                                                '</div>' +
                                                '<div class="class-num">' +
                                                    classObj.student_amount +'人' +
                                                '</div>' +
                                            '</div>' +
                                        '</div>' +
                                    '</div>' +
                                '</li> ';
                        }
                    }
                    _html += '</ul>';
                };
                $('.acc-modal-class .modal-2 .right-class .card-core').html(_html);
                $('.acc-modal-class .modal-2 .right-class').mCustomScrollbar();
                $('.acc-modal-class .modal-2 .right-class li[role="choose_class"]').unbind().on('click', function () {
                    $(this).toggleClass('active');
                })
            }
            //绑定事件
            function bindEvent(){
                //管理我的班级-管理班级（添加班级）
                $('.acc-modal-class .modal-1 .add-btn').unbind().on('click', function () {
                    $('.acc-modal-class .modal-1').css('display','none');
                    $('.acc-modal-class .modal-2').css('display','block');
                    layer.title('添加授课班级',layer_class);
                    get_all_grade_list();
                    get_all_class_list();
                });
                //管理我的班级-管理授课班级 (班级标签删除)
                $('.acc-modal-class .modal-1 .remove').unbind().on('click', function () {
                    $('.acc-modal-class .modal-1').css('display','none');
                    $('.acc-modal-class .modal-3').css('display','block');
                    layer.title('删除授课班级',layer_class);
                    var class_id = $(this).attr('class-id');
                    var class_name = $(this).attr('class-name');
                    $('.acc-modal-class .modal-3 input[name="m3-class-id"]').val(class_id);
                    var info = '删除班级 ['+ class_name +']，将不再此班级授课 ！'
                    $('.acc-modal-class .modal-3 .alarm-info').html(info);
                });
                //管理我的班级-管理授课班级（关闭）
                $('.acc-modal-class .modal-1 .close-btn').unbind().on('click', function () {
                    layer.close(layer_class);
                });
                //管理我的班级-添加授课班级（确定）
                $('.acc-modal-class .modal-2 .confirm-btn').unbind().on('click', function () {
                    var class_id_list = [];
                    $('.acc-modal-class .modal-2 .right-class li[role="choose_class"].active').each(function(index,element) {
                        var class_id = $(element).attr('class-id');
                        if (class_id){
                            class_id_list.push( parseInt(class_id) );
                        }
                    });
                    if ( class_id_list.length <= 0 ) {
                        layer.msg('未选择班级');
                        return;
                    }
                    //添加班级
                    $.ajax({
                        url: '/user_center/api/add/teacher_class',
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            class_id_list: JSON.stringify(class_id_list)
                        },
                        error: function(data) {
                            console.log('请求超时');
                        },
                        success: function(data) {
                            if (data.c != 0) {
                                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                                layer.msg('操作失败,错误代码[' + data.c + ']' + data.m);
                            }else{
                                layer.msg('添加成功');
                                $('.acc-modal-class .modal-1').css('display','block');
                                $('.acc-modal-class .modal-2').css('display','none');
                                layer.title('授课班级管理',layer_class);
                                //刷新数据，回到modal-1
                                init_acc_class();
                                refresh();
                            }
                        }
                    });
                });
                //管理我的班级-添加授课班级（取消）
                $('.acc-modal-class .modal-2 .cancel-btn').unbind().on('click', function () {
                    //回到modal-1
                    $('.acc-modal-class .modal-1').css('display','block');
                    $('.acc-modal-class .modal-2').css('display','none');
                    layer.title('授课班级管理',layer_class);
                });
                //管理我的班级-删除授课班级（确定）
                $('.acc-modal-class .modal-3 .confirm-btn').unbind().on('click', function () {
                    //删除班级
                    var class_id_list = [];
                    var class_id = $('.acc-modal-class .modal-3 input[name="m3-class-id"]').val();
                    if (class_id){
                        class_id_list.push(parseInt(class_id));
                    }
                    $.ajax({
                        url: '/user_center/api/delete/teacher_class',
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            class_id_list: JSON.stringify(class_id_list)
                        },
                        error: function(data) {
                            console.log('请求超时');
                        },
                        success: function(data) {
                            if (data.c != 0) {
                                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                                layer.msg('操作失败,错误代码[' + data.c + ']' + data.m);
                            }else{
                                layer.msg('删除成功');
                                $('.acc-modal-class .modal-1').css('display','block');
                                $('.acc-modal-class .modal-3').css('display','none');
                                layer.title('管理班级',layer_class);
                                //刷新数据，回到modal-1
                                init_acc_class();
                                refresh();
                            }
                        }
                    });
                });
                //管理我的班级-删除授课班级（取消）
                $('.acc-modal-class .modal-3 .cancel-btn').unbind().on('click', function () {
                    //回到modal-1
                    $('.acc-modal-class .modal-1').css('display','block');
                    $('.acc-modal-class .modal-3').css('display','none');
                    layer.title('管理班级',layer_class);
                });

            }
        }
        /*
        身份 ===================================================================================================================
        */
        function init_acc_identity(){
            get_user_type_list();
            //获取当前用户的角色列表
            function get_user_type_list(){
                var type_list = [];
                $.ajax({
                    url: '/user_center/api/list/user_type',
                    type: 'POST',
                    dataType: 'json',
                    data: {},
                    error: function(data) {
                        console.log('请求超时');
                        layer.msg("请求超时");
                    },
                    success: function(data) {
                        if(data.c == 0){
                            type_list = data.d;
                            var user_type_list = formatThis(type_list);
                            var html = gen_user_type_list_html(user_type_list);
                            $('#type-list-form-div').html( html );
                            //滚动条
                            $("#type-list-form-div-container").mCustomScrollbar();
                            bindEvent();
                        }else{
                            console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                            layer.msg('操作失败：' + data.m)
                        }
                    }
                });
            }
            //转化
            function formatThis(type_list){
                // 转换格式
                var ret_type_list = [];
                for (var i in type_list){
                    var ret_type_obj = null;
                    for (var j in ret_type_list){
                        if (type_list[i].school_id == ret_type_list[j].school_id){
                            ret_type_obj = ret_type_list[j]
                        }
                    }
                    if (ret_type_obj == null) {
                        var ret_type_obj = new Object()
                        ret_type_obj.school_id = type_list[i].school_id;
                        ret_type_obj.school_name = type_list[i].school_name;
                        ret_type_obj.type_list = []
                        ret_type_list.push(ret_type_obj)
                    }
                    var type_info = new Object();
                    type_info.type_id = type_list[i].type_id;
                    type_info.type_name = type_list[i].type_name;
                    type_info.full_name = type_list[i].full_name;
                    ret_type_obj.type_list.push(type_info)
                }
                return ret_type_list;
            }
            //渲染角色列表
            function gen_user_type_list_html(user_type_list) {
                var html = '';
                for (var i in user_type_list) {
                    var school_id = user_type_list[i].school_id;
                    var school_name = user_type_list[i].school_name;
                    var type_list = user_type_list[i].type_list;
                    html += '<ul class="list-form-ul">';
                    html += '<li class="list-form-li-first">';
                    html += '<label>' + school_name + '</label>';
                    html += '</li>';
                    for (var j in type_list) {
                        var type_id = type_list[j].type_id;
                        var type_name = type_list[j].type_name;
                        var full_name = type_list[j].full_name;
                        var image_src = "";
                        if (type_name == "学生")
                            image_src = "/static/resources/common/resources/images/icon-head-man.png";
                        else if (type_name == "教师")
                            image_src = "/static/resources/common/resources/images/icon-head-manage.png";
                        else
                            image_src = "/static/resources/common/resources/images/icon-head-woman.png";
                        var radio_checked = "";
                        if (school_id == $("#current_school_id").val() && type_id == $("#current_type_id").val()){
                            radio_checked = "checked";
                        }
                        html += '<li class="list-form-li-other">';
                        html += '<div class="list-form-li-img">';
                        html += '<img src="' + image_src + '">';
                        html += '</div>';
                        html += '<div class="list-form-li-lbl">';
                        html += '<label class="lbl-role">' + type_name + '</label>';
                        html += '<label class="lbl-name">' + full_name + '</label>';
                        html += '</div>';
                        html += '<div class="list-form-li-radio">';
                        html += '<input type="hidden" value="' + school_id + '" id="school_id">';
                        html += '<input type="hidden" value="' + type_id + '" id="type_id">';
                        html += '<input type="radio" name="user_type_radio" ' + radio_checked + '></div>'
                        html += '</li>'
                    }
                    html += "</ul>"
                }
                return html;
            };
            //切换用户角色
            function change_user_type(){
                $('body').showLoading();
                var select_radio = $("input[type='radio']:checked");
                var type_id = select_radio.prevAll('#type_id').val();
                var school_id = select_radio.prevAll('#school_id').val();
                $.ajax({
                    url: "/user_center/api/change/user_type",
                    type: 'POST',
                    data: {school_id: school_id, type_id: type_id},
                    error: function (data) {
                        console.log('请求超时');
                    },
                    success: function(data){
                        if (data.c == 0){
                            layer.close(layer_identity);
                            layer.msg('切换用户角色成功！', {
                                anim:6,
                                time:3000,
                                skin:'layui-layer-hui'
                            },function(){
                                window.location.reload();
                            });
                        }
                    },
                    complete: function(){
                        $('body').hideLoading();
                    }
                });
            }
            //绑定事件
            function bindEvent(){
                //radio
                $('#type-list-form-div .list-form-li-other').unbind().on('click',function(){
                    $('input[type="radio"][name="user_type_radio"]').prop("checked",false);
                    var el= $(this).children('div.list-form-li-radio').children('input[type="radio"]');
                    el.prop("checked",true);
                });
                //确定
                $('#acc-modal-identity .confirm-btn').unbind().on('click', function () {
                    change_user_type();
                });
                //取消
                $('#acc-modal-identity .cancel-btn').unbind().on('click', function () {
                    layer.close(layer_identity);
                });
            }
        }
        /*
        教材 ===================================================================================================================
        */
        function init_acc_textbook(){
            //管理我的教材-管理教材（教材列表）
            $.ajax({
                url: '/user_center/api/list/teacher_textbook',
                type: 'POST',
                dataType: 'json',
                data: {},
                error: function(data) {
                    console.log('请求超时');
                },
                success: function(data) {
                    if (data.c != 0) {
                        console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                    }else{
                        var textbook_list = data.d;
                        console.log()
                        reset_textbook_ul(textbook_list);
                        bindEvent();
                    }
                }
            });
            //管理我的教材-添加教材-年级option
            (function () {
                $.ajax({
                    url:'/user_center/api/list/grade',
                    type: 'POST',
                    dataType: 'json',
                    data: {},
                    error: function(data) {
                        console.log('请求超时');
                    },
                    success: function(data) {
                        if (data.c == 0){
                            var grade_list = data.d;
                            var _html = '<option value="">--请选择--</option>';
                            for (var i=0; i<grade_list.length; i++){
                                var grade = grade_list[i];
                                _html += '<option value="'+grade.grade_num+'">'+grade.grade_name+'</option>'
                            }
                            $('.acc-modal-textbook .modal-2 select[name="m2-grade"]').html(_html);
                        }
                    }
                })
            })();
            //管理我的教材-添加教材-科目option
            (function () {
                $.ajax({
                    type: 'POST',
                    dataType: 'json',
                    url:'/user_center/api/school_list/subject',
                    data:'',
                    success:function(data) {
                        if (data.c == 0){
                            var subject_list = data.d;
                            reset_subject_select(subject_list);
                        }
                    }
                });
            })();
            //管理我的教材-添加教材-教材option
            (function () {
                $.ajax({
                    type: 'POST',
                    dataType: 'json',
                    url:'/user_center/api/school_list/textbook',
                    data:'',
                    success:function(data) {
                        if (data.c == 0){
                            var textbook_list = data.d;
                            reset_textbook_select(textbook_list);
                        }
                    }
                });
            })();

            function reset_textbook_ul(textbook_list){
                var _html = '';
                if (textbook_list.length > 0){
                    _html += '<ul>';
                    for(var i=0; i<textbook_list.length; i++){
                        var textbook = textbook_list[i];
                        _html +=
                            '<li>' +
                                '<div class="s-box">' +
                                    '<span class="s-subject">'+ textbook.subject_name +'</span>' +
                                    '<span class="s-name">'+ textbook.textbook_name +'</span>' +
                                    (textbook.is_current ?
                                            '<img class="s-active-icon" src="/static/resources/common/resources/images/icon-active.png">'
                                            :'<span textbook-id="'+ textbook.textbook_id +'" class="s-usebtn">使用教材</span>') +
                                    (textbook.is_current ?
                                            '':'<el textbook-id="'+ textbook.textbook_id +'" textbook-name="' + textbook.textbook_name + '" class="remove">×</el>')+
                                '</div>' +
                            '</li>';
                        //s-box noback
                        if (textbook.is_current){
                            var _text = '';
                            _text += '<span class="s-subject">'+ textbook.subject_name +'</span>';
                            _text += '<span class="s-name">'+ textbook.textbook_name +'</span>'
                            $('.acc-modal-textbook .modal-1 .s-box.noback').html(_text);
                        }
                    }
                    _html += '</ul>';
                }
                $('.acc-modal-textbook .modal-1 .d-box').html(_html);
                $('.acc-modal-textbook .modal-1 .d-box').mCustomScrollbar();
            }
            //绑定事件
            function bindEvent(){
                //管理我的教材-管理教材（添加教材）
                $('.acc-modal-textbook .modal-1 .add-btn').unbind().on('click', function () {
                    $('.acc-modal-textbook .modal-1').css('display','none');
                    $('.acc-modal-textbook .modal-2').css('display','block');
                    layer.title('添加教材',layer_textbook);
                });
                //管理我的教材-管理教材 (使用教材)
                $('.acc-modal-textbook .modal-1 .s-usebtn').unbind().on('click', function () {
                    var textbook_id = parseInt($(this).attr('textbook-id'));
                    $.ajax({
                        url: '/user_center/api/update/teacher_textbook',
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            textbook_id: textbook_id
                        },
                        error: function(data) {
                            console.log('请求超时');
                        },
                        success: function(data) {
                            if (data.c != 0) {
                                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                            }else{
                                layer.msg('操作成功');
                                //重新渲染
                                init_acc_textbook();
                                refresh();
                            }
                        }
                    });
                });
                //管理我的教材-管理教材 (教材标签删除)
                $('.acc-modal-textbook .modal-1 .remove').unbind().on('click', function () {
                    $('.acc-modal-textbook .modal-1').css('display','none');
                    $('.acc-modal-textbook .modal-3').css('display','block');
                    layer.title('删除教材',layer_textbook);
                    var textbook_id = $(this).attr('textbook-id');
                    var textbook_name = $(this).attr('textbook-name');
                    $('.acc-modal-textbook .modal-3 input[name="m3-textbook-id"]').val(textbook_id);
                    var info = '删除教材 ['+ textbook_name +'] 并保留相关资源，下次添加时相关资源依然存在无需再次上传！'
                    $('.acc-modal-textbook .modal-3 .alarm-info').html(info);
                });
                //管理我的教材-管理教材（关闭）
                $('.acc-modal-textbook .modal-1 .close-btn').unbind().on('click', function () {
                    layer.close(layer_textbook);
                });
                //管理我的教材-添加教材（确定）
                $('.acc-modal-textbook .modal-2 .confirm-btn').unbind().on('click', function () {
                    //校验
                    var textbook_select = $('.acc-modal-textbook .modal-2 select[name="m2-textbook"]').val()
                    if ( !textbook_select ){
                        layer.msg('教材不允许为空');
                        return;
                    }
                    //添加教材
                    var textbook_id_list = [];
                    var textbook_id = $('.acc-modal-textbook .modal-2 select[name="m2-textbook"]').val();
                    if (textbook_id){
                        textbook_id_list.push(parseInt(textbook_id));
                    }
                    $.ajax({
                        url: '/user_center/api/add/teacher_textbook',
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            textbook_id_list: JSON.stringify(textbook_id_list)
                        },
                        error: function(data) {
                            console.log('请求超时');
                        },
                        success: function(data) {
                            if (data.c != 0) {
                                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                                layer.msg('操作失败,错误代码[' + data.c + ']' + data.m);
                            }else{
                                layer.msg('添加成功');
                                $('.acc-modal-textbook .modal-1').css('display','block');
                                $('.acc-modal-textbook .modal-2').css('display','none');
                                layer.title('管理教材',layer_textbook);
                                //刷新数据，回到modal-1
                                init_acc_textbook();
                                refresh();
                            }
                        }
                    });
                });
                //管理我的教材-添加教材（取消）
                $('.acc-modal-textbook .modal-2 .cancel-btn').unbind().on('click', function () {
                    //回到modal-1
                    $('.acc-modal-textbook .modal-1').css('display','block');
                    $('.acc-modal-textbook .modal-2').css('display','none');
                    layer.title('管理教材',layer_textbook);
                });
                //管理我的教材-删除教材（确定）
                $('.acc-modal-textbook .modal-3 .confirm-btn').unbind().on('click', function () {
                    //删除教材
                    var textbook_id_list = [];
                    var textbook_id = $('.acc-modal-textbook .modal-3 input[name="m3-textbook-id"]').val();
                    if (textbook_id){
                        textbook_id_list.push(parseInt(textbook_id));
                    }
                    $.ajax({
                        url: '/user_center/api/delete/teacher_textbook',
                        type: 'POST',
                        dataType: 'json',
                        data: {
                            textbook_id_list: JSON.stringify(textbook_id_list)
                        },
                        error: function(data) {
                            console.log('请求超时');
                        },
                        success: function(data) {
                            if (data.c != 0) {
                                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                                layer.msg('操作失败,错误代码[' + data.c + ']' + data.m);
                            }else{
                                layer.msg('删除成功');
                                $('.acc-modal-textbook .modal-1').css('display','block');
                                $('.acc-modal-textbook .modal-3').css('display','none');
                                layer.title('管理教材',layer_textbook);
                                //刷新数据，回到modal-1
                                init_acc_textbook();
                                refresh();
                            }
                        }
                    });
                });
                //管理我的教材-删除教材（取消）
                $('.acc-modal-textbook .modal-3 .cancel-btn').unbind().on('click', function () {
                    //回到modal-1
                    $('.acc-modal-textbook .modal-1').css('display','block');
                    $('.acc-modal-textbook .modal-3').css('display','none');
                    layer.title('管理教材',layer_textbook);
                });
                //管理我的教材-添加教材（年级select改变）
                $('.acc-modal-textbook .modal-2 select[name="m2-grade"]').unbind().on('change', function () {
                    reload_textbook_list();
                });
                //管理我的教材-添加教材（科目select改变）
                $('.acc-modal-textbook .modal-2 select[name="m2-subject"]').unbind().on('change', function () {
                    reload_textbook_list();
                });
            }

            function reset_subject_select(subject_list){
                var _html = '<option value="">--请选择--</option>';
                for (var i=0; i<subject_list.length; i++){
                    var subject = subject_list[i];
                    _html += '<option value="'+subject.id+'">'+subject.name+'</option>'
                }
                $('.acc-modal-textbook .modal-2 select[name="m2-subject"]').html(_html);
            }

            function reset_textbook_select(textbook_list){
                var _html = '<option value="">--请选择--</option>';
                for (var i=0; i<textbook_list.length; i++){
                    var textbook = textbook_list[i];
                    _html += '<option value="'+textbook.id+'">'+textbook.textbook_name+'</option>'
                }
                $('.acc-modal-textbook .modal-2 select[name="m2-textbook"]').html(_html);
            }

            function reload_textbook_list(){
                var grade_num = $('.acc-modal-textbook .modal-2 select[name="m2-grade"]').val();
                var subject_id = $('.acc-modal-textbook .modal-2 select[name="m2-subject"]').val();
                var grade_num_list = [];
                var subject_id_list = [];
                if(grade_num){
                    grade_num_list.push(grade_num);
                }
                if(subject_id){
                    subject_id_list.push(subject_id);
                };
                $.ajax({
                    url:'/user_center/api/school_list/textbook',
                    type: 'POST',
                    dataType: 'json',
                    data:{
                        not_belong_flag: 0,
                        grade_num_list: JSON.stringify(grade_num_list),
                        subject_id_list: JSON.stringify(subject_id_list)
                    },
                    error: function(data) {
                        console.log('请求超时');
                        layer.msg('请求超时');
                    },
                    success: function(data) {
                        if (data.c == 0){
                            var textbook_list = data.d;
                            reset_textbook_select(textbook_list);
                        }else{
                            console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                            layer.msg('操作失败,错误代码[' + data.c + ']' + data.m);
                        }
                    }
                })
            }
        }

        (function() {
            getUserCenterUrl();
            initAccount();
        })();

        return {
            loadrightTab: loadrightTab,
            refresh: refresh,
            getAccount: getAccount,
        };

    }
});

$(function(o){
   /**app列表**/
   $('.mytooltip-logo').on('mouseenter',function(){
      $('#hx-logo-triangle-default').attr("hidden","hidden");
      $('#hx-logo-triangle-visited').removeAttr("hidden");
      $('.hx-app-list-container').removeAttr("hidden");
      //获取app_list
      get_service_apps();
   });
   $('.mytooltip-logo').on('mouseleave',function(){
      $('#hx-logo-triangle-default').removeAttr("hidden");
      $('#hx-logo-triangle-visited').attr("hidden","hidden");
      $('.hx-app-list-container').attr("hidden","hidden");
   });
   /**account列表**/
   o.HX_COM_ACCOUNT = $.hxComAccount();
   $('.mytooltip-acc').on('mouseenter',function(){
      $('#hx-account-triangle-default').attr("hidden","hidden");
      $('#hx-account-triangle-visited').removeAttr("hidden");
      $('.hx-layer-account-container').removeAttr("hidden");
      HX_COM_ACCOUNT.loadrightTab();
   });
   $('.mytooltip-acc').on('mouseleave',function(){
      $('#hx-account-triangle-visited').attr("hidden","hidden");
      $('#hx-account-triangle-default').removeAttr("hidden");
      $('.hx-layer-account-container').attr("hidden","hidden");
   });
}(window));

//获取app列表
function get_service_apps(){
   if (!window.HX_SERVICE_APPS_FLAG){
      var container = $('.hx-app-list-container');
      $(container.children('.loading-gif')).remove();
      container.prepend('<div class="loading-gif"><img src="/static/resources/common/resources/images/loading-cricle.gif"></div>');
      $.ajax({
         url: '/user_center/api/list/service_apps',
         data: {},
         type: 'POST',
         error: function (data) {
            console.log('请求超时');
         },
         success: function (data) {
            if (data.c == 0){
               var app_list_data = data.d;
                $(container.children('.loading-gif')).remove();
                reset_applist_ul(app_list_data);
                window.HX_SERVICE_APPS_FLAG = true;
            }else{
               console.log('操作失败,错误代码[' + data.c + ']' + data.m);
            }
         }
      });
   }
    function reset_applist_ul(app_list_data){
        var el_html = '';
        for(var k in app_list_data){
          var category = app_list_data[k].category ,app_list = app_list_data[k].data;
          (function () {
             el_html += '<div class="hx-one-category">';
                el_html += '<div class="hx-category-title">'+category+'</div>';
                el_html += '<ul>';
                for (var index in app_list){
                   var appObj = app_list[index];
                   var jump = 'window.location.href=\''+appObj.url+'\'';
                   if (appObj.type == 2){
                      jump = 'window.open(\''+appObj.url+'\')';
                   }
                   el_html += ''
                     +'<li class="hx-app-list-cell" onclick="javascript:'+jump+'">'
                         +'<div class="cell-box">'
                             +'<img src="'+appObj.image_url+'">'
                             +'<span class="cell-box-text">'+appObj.name+'</span>'
                         +'</div>'
                     +'</li>'
                };
                el_html += '</ul>';
             el_html += '</div>';
          }());
        }
        var inner_box = $('.hx-app-list-container .hx-inner-box');
        if( inner_box.find('.mCustomScrollBox').length <= 0 ){
            inner_box.html(el_html);
            inner_box.mCustomScrollbar();
        };
   }
}


