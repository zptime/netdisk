/**
 * Created by jie on 2017/6/1.
 */

//选择部门和用户
(function ($) {
    $.extend({
        chooseDepartAndUser: function (options) {
            // default plugin settings
            var defaults = {
                type: 1, //1 只选部门   2 选部门和老师  3 只选老师
                title:"发送对象",
            };

            var opts = $.extend(defaults, options);

            function init(){
                var _html= '';
                _html+='<div class="box box-'+defaults.type+'">';
                _html+='<div class="box-left ztree" id="left"><div class="box-left-inpbox"><input type="text " id="nameSearch" class="name-search-input" placeholder="请输入姓名"  ></div><ul id="leftSend" class="ztree ztree-send"></ul></div>';
                _html+='<div class="box-right" id="right"><div id="rightSend"><ul></ul></div></div>';
                _html+='</div>';
                $.ajax({
                    url:'/api/list/send_target',
                    type:'post',
                    data:{},
                    success: function (json) {
                        if(json.c==0){
                            json.d[0].open=true;
                            var tempData = [];
                            for(var i in json.d){
                                if(json.d[i].object_type=="1"){
                                    tempData.push(json.d[i])
                                }
                            };
                            for(var i in json.d){
                                if(json.d[i].object_type=="2"){
                                    tempData.push(json.d[i])
                                }
                            }
                            json.d = tempData;
                            if (opts.type == 1){ //只选择部门
                                var data = json.d;
                                var arr =[];
                                for(var i in data){
                                    if(data[i].object_type=="1"){
                                        arr.push(data[i]);
                                    }
                                }
                                ztreeInit("leftSend",arr);
                            }else if (opts.type == 2){ //选择部门和老师
                                var data = json.d;
                                var arr =[];
                                for(var i = 0 ;i<data.length;i++){
                                    data[i].open=true;
                                    if(data[i].object_type=="2"){
                                        data[i].trueId=data[i].id;
                                        data[i].id="teacher_"+data[i].id;
                                        arr.push(data[i])
                                    }else{
                                       arr.push(data[i])
                                    }
                                }
                                ztreeInit("leftSend",data);
                            }else if (opts.type == 3){ //只选择老师
                                var data = json.d;
                                var arr =[];
                                for(var i in data){
                                    if(data[i].object_type=="1"){
                                        data[i].nocheck=true;
                                        arr.push(data[i]);
                                    }else{
                                        data[i].trueId = data[i].id;
                                        data[i].id = "teacher_"+data[i].id;
                                        arr.push(data[i]);
                                    }
                                }
                                ztreeInit("leftSend",arr);
                            }
                        }else{
                            layer.msg("请求出错!")
                        }
                    }
                });
                layer.open({
                    type: 1,
                    content:_html,
                    btn:["确定","取消"],
                    area:["800px","500px"],
                    title:opts.title,
                    yes:function (index) {
                        if ( typeof(opts.confirm) == 'function' ){
                            opts.confirm();
                        }
                        layer.close(index);
                    }
                });

            };

            function ztreeInit(treeDemo,zNodes,setting){
                var curMenu = null, zTree_Menu = null;
                if(!setting){
                    var setting = {
                        view: {
                            selectedMulti: false,
                            fontCss: getFontCss,
                            showLine: false,
                            showIcon: false,
                            dblClickExpand: false,
                            showTitle: false,
                        },
                        check: {
                          enable: true,
                          //chkboxType : { "Y" : "", "N" : "" },
                        },
                        edit: {
                            enable: true,
                            showRemoveBtn: false,
                            showRenameBtn: false
                        },
                        data: {
                            key: {
                                title: "fullName"
                            },
                            keep: {
                                parent:true,
                                leaf:true
                            },
                            simpleData: {
                                enable: true
                            }
                        },
                        callback: {
                            beforeDrag: beforeDrag,
                            beforeRemove: beforeRemove,
                            beforeRename: beforeRename,
                            onRemove: onRemove,
                            onCheck: addToRight,
                            onClick: onClick
                        }
                    };
                    if (opts.type == 1){ //只选择部门,不影响父子节点
                        setting.check['chkboxType'] = { "Y" : "", "N" : "" }
                    };
                    if (opts.type == 3){ //只选择老师,不影响父子节点
                        setting.check['chkboxType'] = { "Y" : "", "N" : "" }
                        if(opts.radio == "teacher"){
                         setting.check['chkStyle']  =   "radio";
                         setting.check['radioType']  =   "all";
                        }
                    };
                }
                if(!zNodes){
                    var zNodes =[
                        { id:1, pId:0, name:"parent node 1", open:true},
                        { id:11, pId:1, name:"leaf node 1-1"},
                        { id:12, pId:1, name:"leaf node 1-2"},
                        { id:13, pId:1, name:"leaf node 1-3"},
                        { id:2, pId:0, name:"parent node 2", open:true},
                        { id:21, pId:2, name:"leaf node 2-1"},
                        { id:22, pId:2, name:"leaf node 2-2"},
                        { id:23, pId:2, name:"leaf node 2-3"},
                        { id:3, pId:0, name:"parent node 3", open:true },
                        { id:31, pId:3, name:"leaf node 3-1"},
                        { id:32, pId:3, name:"leaf node 3-2"},
                        { id:33, pId:3, name:"leaf node 3-3"}
                    ];
                }
                var log, className = "dark";
                function beforeDrag(treeId, treeNodes) {
                    return false;
                }
                function beforeRemove(treeId, treeNode) {
                    className = (className === "dark" ? "":"dark");
                    showLog("[ "+getTime()+" beforeRemove ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
                    return confirm("Confirm delete node '" + treeNode.name + "' it?");
                }
                function onRemove(e, treeId, treeNode) {
                    showLog("[ "+getTime()+" onRemove ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
                }
                function beforeRename(treeId, treeNode, newName) {
                    if (newName.length == 0) {
                        alert("Node name can not be empty.");
                        var zTree = $.fn.zTree.getZTreeObj(treeDemo);
                        setTimeout(function(){zTree.editName(treeNode)}, 10);
                        return false;
                    }
                    return true;
                }
                function showLog(str) {
                    if (!log) log = $("#log");
                    log.append("<li class='"+className+"'>"+str+"</li>");
                    if(log.children("li").length > 8) {
                        log.get(0).removeChild(log.children("li")[0]);
                    }
                }
                function getTime() {
                    var now= new Date(),
                    h=now.getHours(),
                    m=now.getMinutes(),
                    s=now.getSeconds(),
                    ms=now.getMilliseconds();
                    return (h+":"+m+":"+s+ " " +ms);
                }
                function add(e) {
                    var zTree = $.fn.zTree.getZTreeObj(treeDemo),
                    isParent = e.data.isParent,
                    nodes = zTree.getSelectedNodes(),
                    treeNode = nodes[0];
                    if (treeNode) {
                        treeNode = zTree.addNodes(treeNode, {id:(100 + newCount), pId:treeNode.id, isParent:isParent, name:"new node" + (newCount++)});
                    } else {
                        treeNode = zTree.addNodes(null, {id:(100 + newCount), pId:0, isParent:isParent, name:"new node" + (newCount++)});
                    }
                    if (treeNode) {
                        zTree.editName(treeNode[0]);
                    } else {
                        alert("Leaf node is locked and can not add child node.");
                    }
                };
                function onClick(e,treeId, treeNode) {
                    var zTree = $.fn.zTree.getZTreeObj(treeDemo);
                    zTree.expandNode(treeNode);
                    if(treeNode.children&&treeNode.children.length>0){
                        //
                    }else{
                        if(opts.radio == "teacher" ){
                            var tRadio ="#" + treeNode.tId +"_check"
                            $(tRadio).click();
                        }

                    }
                }
                function edit() {
                    var zTree = $.fn.zTree.getZTreeObj(treeDemo),
                    nodes = zTree.getSelectedNodes(),
                    treeNode = nodes[0];
                    if (nodes.length == 0) {
                        alert("Please select one node at first...");
                        return;
                    }
                    zTree.editName(treeNode);
                };
                function remove(e) {
                    var zTree = $.fn.zTree.getZTreeObj(treeDemo),
                    nodes = zTree.getSelectedNodes(),
                    treeNode = nodes[0];
                    if (nodes.length == 0) {
                        alert("Please select one node at first...");
                        return;
                    }
                    var callbackFlag = $("#callbackTrigger").attr("checked");
                    zTree.removeNode(treeNode, callbackFlag);
                };
                function clearChildren(e) {
                    var zTree = $.fn.zTree.getZTreeObj(treeDemo),
                    nodes = zTree.getSelectedNodes(),
                    treeNode = nodes[0];
                    if (nodes.length == 0 || !nodes[0].isParent) {
                        alert("Please select one parent node at first...");
                        return;
                    }
                    zTree.removeChildNodes(treeNode);
                };
                function addToRight(e,treeId, treeNode){
                    if (opts.type == 1){ //只选择部门
                        var zTree = $.fn.zTree.getZTreeObj(treeDemo),
                        nodes = zTree.getCheckedNodes(true);
                        var arr=[];
                        $("#rightSend ul").html("");
                        for(var i in nodes){
                                    var a = ' <li class="item-p item" dataid="' + nodes[i].id + '"  ><span class="item-name">' + nodes[i].name + '</span><b dataid="'+nodes[i].tId+'"  class="item-delete"  >x</b></li>'//
                                    $("#rightSend ul").append(a);
                        }
                        $("#rightSend .item-delete").click(function () {
                            var tId = $(this).attr("dataid");
                            $("#"+tId+"_check").click();
                        });
                    }else if(opts.type == 2){ //选择部门和教师
                        var zTree = $.fn.zTree.getZTreeObj(treeDemo),
                        nodes = zTree.getCheckedNodes(true);
                        var arr=[];
                        $("#rightSend ul").html("");
                        for(var i in nodes) {
                            if (nodes[i].isParent && nodes[i].check_Child_State == 2) {
                                if (!nodes[i].getParentNode()) {
                                    var a = ' <li class="item-p item" dataname="'+nodes[i].name+'"  dataimage_url="'+nodes[i].image_url+'"   dataid="' + nodes[i].id + '"  ><span class="item-name">' + nodes[i].name + '</span><b dataid="'+nodes[i].tId+'"    class="item-delete"  >x</b></li>'//
                                    $("#rightSend ul").append(a);
                                    arr.push(nodes[i].id);
                                    break;
                                } else if (nodes[i].getParentNode().check_Child_State !== 2) {
                                    var a = ' <li class="item-p item" dataname="'+nodes[i].getParentNode().name+'" dataimage_url="'+nodes[i].image_url+'"   dataid="' + nodes[i].id + '"  ><span class="item-name">' + nodes[i].name + '</span><b dataid="'+nodes[i].tId+'"   class="item-delete" >x</b></li>'//
                                    $("#rightSend ul").append(a);
                                    arr.push(nodes[i].id);
                                }
                            }
                        };
                        for(var i in nodes){
                            if(!nodes[i].isParent&&nodes[i].getParentNode().check_Child_State !== 2&&nodes[i].object_type=="1"){
                                    var a = ' <li class="item item-p" dataname="'+nodes[i].getParentNode().name+'"  dataimage_url="'+nodes[i].image_url+'"   dataid="'+nodes[i].id+'"  ><span class="item-name">'+nodes[i].name+'</span><b dataid="'+nodes[i].tId+'"   class="item-delete"  >x</b></li>'//
                                    $("#rightSend ul").append(a);
                            }
                        }
                        for(var i in nodes){
                            if(!nodes[i].isParent&&nodes[i].getParentNode().check_Child_State !== 2&&nodes[i].object_type=="2"){
                                    var a = ' <li class="item item-person" dataname="'+nodes[i].getParentNode().name+'" dataimage_url="'+nodes[i].image_url+'"    dataid="'+nodes[i].id+'"  ><span class="item-name">'+nodes[i].name+'</span><b dataid="'+nodes[i].tId+'" class="item-delete"  >x</b></li>'//
                                    $("#rightSend ul").append(a);
                            }
                        }
                        $("#rightSend .item-p:last").after('<li style="display:block;height:1px;background:#ccc;margin:20px 0;" ></li>')
                        $("#rightSend .item-delete").click(function () {
                            var tId = $(this).attr("dataid");
                            $("#"+tId+"_check").click();

                        });
                    }else if(opts.type == 3){ //只选择教师
                        var zTree = $.fn.zTree.getZTreeObj(treeDemo),
                        nodes = zTree.getCheckedNodes(true);
                        var arr=[];
                        $("#rightSend ul").html("");
                        for(var i in nodes){
                            var a = ' <li class="item item-person" dataname="'+nodes[i].getParentNode().name+'"  dataimage_url="'+nodes[i].image_url+'"   dataid="'+nodes[i].id+'"  ><span class="item-name">'+nodes[i].name+'</span><b dataid="'+nodes[i].tId+'" class="item-delete"  >x</b></li>'//
                            $("#rightSend ul").append(a);
                        }
                        $("#rightSend .item-delete").click(function () {
                            $(this).parent().remove();
                            var tId = $(this).attr("dataid");
                            $("#"+tId+"_check").click();
                        });
                    }
                }

                function addDiyDom(treeId, treeNode) {
                    var spaceWidth = 5;
                    var switchObj = $("#" + treeNode.tId + "_switch"),
                    icoObj = $("#" + treeNode.tId + "_ico");
                    switchObj.remove();
                    icoObj.before(switchObj);
                    if (treeNode.level > 1) {
                        var spaceStr = "<span style='display: inline-block;width:" + (spaceWidth * treeNode.level)+ "px'></span>";
                        switchObj.before(spaceStr);
                    }
                }


                //   查找ztree部分
                function focusKey(e) {
                    if (key.hasClass("empty")) {
                        key.removeClass("empty");
                    }
                }
                function blurKey(e) {
                    if (key.get(0).value === "") {
                        key.addClass("empty");
                    }
                }
                var lastValue = "", nodeList = [], fontCss = {};
                function searchNode(e) {
                    var zTree = $.fn.zTree.getZTreeObj(treeDemo);
                        var value = $.trim(key.get(0).value);
                        var keyType = "";
                        keyType = "name";
                        if (key.hasClass("empty")) {
                            value = "";
                        }
                        if (lastValue === value) return;
                        lastValue = value;
                        if (value === ""){
                            updateNodes(false);
                           return;
                        }
                        updateNodes(false);
                        nodeList = zTree.getNodesByParamFuzzy(keyType, value)
                        updateNodes(true);
                }
                function updateNodes(highlight) {
                    var zTree = $.fn.zTree.getZTreeObj(treeDemo);
                    for( var i=0, l=nodeList.length; i<l; i++) {
                        nodeList[i].highlight = highlight;
                        zTree.updateNode(nodeList[i]);
                    }
                }
                function getFontCss(treeId, treeNode) {

                    return (!!treeNode.highlight) ? {color:"#A60000", "font-weight":"bold","height":"30px"} : {color:"#333", "font-weight":"normal","height":"30px"};
                }
                function filter(node) {
                    return !node.isParent && node.isFirstNode;
                }

                $(document).ready(function(){
                    $.fn.zTree.init($("#"+treeDemo), setting, zNodes);
                    var treeObj = $("#"+treeDemo);
                    key = $("#nameSearch");
                    key.bind("focus", focusKey)
                    .bind("blur", blurKey)
                    .bind("propertychange", searchNode)
                    .bind("input", searchNode);

                });
            }

            $(function () {
                init();
            });
        }
    });
})(jQuery);