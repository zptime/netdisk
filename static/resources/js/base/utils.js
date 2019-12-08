/**
 * Created by jie on 2016/10/20.
 */
function getYNname(val) {
    var res = '';
    if (val == '1') {
        res = '是'
    } else if (val == '0') {
        res = '否'
    }
    return res
}
function Serializetojson(str) {
    "use strict";
    str = str.replace(/\+/g," ");
    var res = {},
    arr = decodeURIComponent(str, true).split('&');
    for (var i in arr) {
        var item = arr[i].split('='),
        key = item[0],
        value = item[1];
        res[key] = value
    }
    return res
}
function formatnumber(data, leng){
    var res='',data_str=data.toString(),v_length=leng?leng:2;
    if (data_str.length < v_length){
        for (var i=0; i< v_length - data_str.length; i++ ){
            res += '0';
        }
    }
    res += data_str;
    return res;
}
function url_go(url) {
    window.location.href = encodeURI(url)
}
function url_back() {
    window.history.go( - 1)
}
function mycheck(opt){
    var res = true;
    defaults = {
        element: '#content',
    }
    settings = extend(defaults, opt);
    //校验
    $(settings.element+' label.required').each(function(index,element){
        var el_check = $(element).attr('for');
        if (el_check){
            var el =  $('[check="'+el_check+'"]') ;
            var loop2 = true;
            el.each(function (index2, element2) {
                if ( !$(element2).val() ){
                    layer.msg($(element).text()+'不允许为空');
                    element2.focus();
                    loop2 = false;
                    res = false;
                    return false;
                }
            });
            return loop2;
        }
    });
    return res;
}
function submit_with_parameters(action, method, values) {
    var form = $('<form/>', {
        action: action,
        method: method
    });
    $.each(values, function() {
        form.append($('<input/>', {
            type: 'hidden',
            name: this.name,
            value: this.value
        }));
    });
    form.appendTo('body').submit();
}

function myajax(opt, callback) {
    if (!opt.url) return '未配置url';
    defaults = {
        url: '',
        type: 'POST',
        dataType: 'json',
        complete: function(data) {
            if (typeof callback == 'function') {
                callback(JSON.parse(data.responseText))
            }
            if( opt.loading ){
                $('body').hideLoading();
            }
        },
        error: function(data) {
            console.log('请求超时');
            layer.msg("请求超时");
        },
        success: function(data) {
            if (data.c != 0) {
                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                layer.msg('操作失败：' + data.m)
            }
        }
    };
    var settings = extend(defaults, opt);
    if( opt.loading ){
        $('body').showLoading();
    }
    $.ajax(settings)
}

function myajaxForm(el, opt) {
    if (!opt.url) return '未配置url';
    var defaults = {
        target: '_self',
        success: function(data) {
            if (data.c == 0) {
                if (opt.successed && typeof opt.successed == 'function'){
                    opt.successed(data);
                };
                layer.alert('操作成功', function(index){
                  //do something
                    if (opt.next_path){
                        if (opt.next_path == '_self'){
                            layer.close(index);
                        }else{
                            url_go(opt.next_path);
                        }
                    }else{
                        url_back();
                    }
                });
            } else if (data.c != 0) {
                console.log('操作失败,错误代码[' + data.c + ']' + data.m);
                layer.msg('操作失败：' + data.m)
            }
        },
        url: '',
        type: 'POST',
        dataType: 'json',
        //resetForm: true,
    }
    settings = extend(defaults, opt);
    el.ajaxForm(settings)
}
function extend(target, source) {
    "use strict";
    var property;
    for (property in source) {
        if (source.hasOwnProperty(property)) {
            target[property] = source[property]
        }
    }
    return target
};

function hascheckedrows(callback) {
    var rowIds = $("#grid").getGridParam("selarrrow");
    if (rowIds.length == 0) {
        layer.msg('未选择记录');
        return false
    }
    callback(rowIds);
    return true
}
function hascheckedonerow(callback) {
    var rowIds = $("#grid").getGridParam("selarrrow");
    if (rowIds.length != 1) {
        layer.msg('请选择一条记录');
        return false
    }
    callback(rowIds[0]);
    return true
}


//建立一个可存取到该file的url
function getObjectURL(file) {
  var url = null ;
  if (window.createObjectURL!=undefined) { // basic
    url = window.createObjectURL(file) ;
  } else if (window.URL!=undefined) { // mozilla(firefox)
    url = window.URL.createObjectURL(file) ;
  } else if (window.webkitURL!=undefined) { // webkit or chrome
    url = window.webkitURL.createObjectURL(file) ;
  }
  return url ;
}

//阿拉伯数字转中文数字
function convert_num_to_ch(num){
    ch_num_list = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    if (num >=0 && num <=9){
        return ch_num_list[num];
    } else {
        return num;
    }
}

//获取url
function get_url_path(nav, page) {
    var path = "/?nav=" + nav;
    if (page) {
        path += "&page=";
        path += page
    }
    return path;
}

//转换文件大小单位
function formatBytes(bytes){
      if      (bytes>=1073741824) {bytes=(bytes/1073741824).toFixed(2)+' GB';}
      else if (bytes>=1048576)    {bytes=(bytes/1048576).toFixed(2)+' MB';}
      else if (bytes>=1024)       {bytes=(bytes/1024).toFixed(2)+' KB';}
      else if (bytes>1)           {bytes=bytes+' bytes';}
      else if (bytes==1)          {bytes=bytes+' byte';}
      else                        {bytes='0 byte';}
      return bytes;
}

// windows.open 避免拦截问题
function window_open(url){
    var popup = window.open('about:blank', '_blank');  //先发起弹窗（因为是用户触发，所以不会被拦截）
    popup.location = url;
    $.ajax({
        url: '/get/page',
        type: 'POST',
        dataType: 'json',
        data: {url: url},
        success: function(data){
            debugger;
            popup.location = data.url;  //在重定向页面链接
        }
    })
}