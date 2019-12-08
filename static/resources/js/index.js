/**
 * Created by panguang on 2018/7/24.
 */
$(function () {
    var pathname = window.location.pathname;
    $(".outerbefore-navitem").removeClass("active");
    $(".outerbefore-navbox a").each(function () {
        if($(this).attr("href")==pathname){
            $(this).parent().addClass("active")
        }
    })
})
//删除提示
function delete_layer(data,yesCb,cancelCb){
    var url="/static/resources/images/netdisk/deleteicon.png";
    var content = '<div  style="margin-top: 74px;margin-left: 40px;position: relative">'+
                '<div style="position: absolute;left: 0;top: 0;width: 50px;height: 50px;background: url('+url+') 100% 100%;background-size: 100% 100%;"></div>'+
                '<div style="padding-left: 60px;">'+
                '<div style="font-size: 16px;color: #444444;">确定删除该文件夹?</div>'+
                '<p style="line-height: 24px;color: #888;font-size: 14px;width: 350px;">删除文件后,该文件夹所属所有子文件夹和文件将一并删除,永远不能被找回！</p>'+
                '</div>'+
                '</div>'
    layer.open({
        type:1,
        area:["500px","300px"],
        title:"删除提示",
        btn:["确定","取消"],
        content:content,
        yes: function () {
            yesCb&&yesCb(data);
        },
        cancel: function () {
            cancelCb&&cancelCb(data);
        }
    })
}
//分享地址
function share_layer(data,str,yesCb,cancelCb){
    window.successTip = function(){
         layer.tips('复制成功', $(".copy_link"), {
          tips: [2, '#000'],
          time: 1000
        });
    }    
    var url="/static/resources/images/netdisk/duigou_icon.png";
    if(!str)str='';
    var content = '<div  style="margin-top:30px;margin-left:40px;position: relative">'+
                '<div style="height:30px;line-height:30px;background: url('+url+')no-repeat;background-size: 30px 30px;padding-left: 40px;background-position: left center;font-size: 14px;color: #444;font-weight: bold;">已创建分享链接,复制发给QQ、微信好友吧</div>'+
                '<div style="font-size: 16px;color: #666;height: 30px;border: solid 1px #dcdcdc;padding-left: 10px;line-height: 30px;border-radius: 4px;margin: 10px 0;width: 440px;">'+str+'</div>'+
                '<div style="height: 30px;border-radius: 15px;background: #4685FF;line-height: 30px;color: #fff;text-align: center;cursor: pointer;font-size: 14px;width: 100px;" class="copy_link" onclick="successTip()">复制链接</div>'+
                '<p style="line-height: 24px;color: #aaa;font-size: 14px;width: 440px;margin-top: 30px;">请严格遵守相关法律法规，严禁在互联网上存储、传播涉密、淫秽、盗版侵权、以及危害国家公共安全和社会和谐稳定的内容及信息。</p>'+
                '</div>'
    layer.open({
        type:1,
        area:["520px","330px"],
        title:"分享地址",
        btn:["确定","取消"],
        content:content,
        yes: function () {
            yesCb&&yesCb(data);
        },
        cancel: function () {
            cancelCb&&cancelCb(data);
        }
    })


}

//打开提示无权进去
function noAccess(type){
    var title ='打开提示'
    if(!!type)title='管理提示';

    layer.open({
        type:1,
        area:["520px","330px"],
        title:title,
        btn:["确定"],
        content:'<div style="line-height:200px;text-align:center;color:#444;font-size:16px;font-weight:bold;">您无权访问文件夹</div>',
    })
}

//正在执行的loading
function loading_now(){
    layer.msg('正在执行', {
      icon: 16
      ,shade: 0.01
      ,time: 1000
    });
}

function confirmCallback(){alert(123)}

//$.chooseDepartAndUser({
//    type: 1,
//    confirm: confirmCallback
//});