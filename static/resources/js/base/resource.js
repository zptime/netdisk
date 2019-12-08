/**
 * Created by jie on 2016/10/27.
 */

/*
在此添加或组织全局变量
*/
Vue.config.delimiters = ["{$", "$}"];
var CONST = {
    'Authority': {
        DEPARTMENT : { code:1, name: "部门管理" , style:{class: "tuanduiguanli", color:'#74bb55'} },
        NOTICE : { code:2, name: "通知管理", style:{class: "tongzhi", color:'#ff644f'} },
        DOCUMENT : { code:4, name: "公文管理", style:{class: "gongwenchuli", color:'#ff902d'} }
    },
    'fileIcon': ['DOC','IMG','MP3','MP4','PDF','PPT','ZIP','TXT','XLS'],
    'purchase_type': ['办公用品','网络设备','教学用具','电气设备','其他'],
    'pay_type': ['现金', '汇款', '网络支付'],
    'job_status': [
        {id: 1, name:'审批中'},
        {id: 2, name:'审批完成'},
        {id: 3, name:'已撤销'}
    ],
    'approve_status':[
        {id: 1, name:'未开始', color: '#e5e5e5;'},
        {id: 2, name:'等待审批', color: '#ffab00;'},
        {id: 3, name:'同意', color: '#53b836;'},
        {id: 4, name:'拒绝', color: '#fd5555;'},
        {id: 5, name:'转交', color: '#308ce3;'},
        {id: 6, name:'已撤销', color: '#e5e5e5;'}
    ]
};

/*
在此图片添加路径常量
*/
var ICON = {
    PHOTO_DEFAULT: "/static/resources/images/icon/photo-default.png", //默认头像
}

