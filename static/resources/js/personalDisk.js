/**
 * Created by yulu on 2018/7/25.
 */
$(function() {
    $("#personalDisk").append("<hr>");

    new Vue({
        el: '#main',
        data: {
            keyword: '',
            title:'移动到',
        },
        ready: function () {
            var self = this;

            /*$('.search').keypress(function (event) {
                if (event.keyCode == 13) {
                    $('#queryBtn').click();
                }
            });*/

            //加载grid表格
            /*myjqGrid($('#grid'), {
                url: '/api/repair/buy/list',
                mtype: 'GET',
                postData: {
                    'keyword': self.keyword
                },
                colNames: ['id', '物品名称', '型号与规格', '数量', '预计金额', '维修员', '所属报修单号', '填单时间'],
                colModel: [
                    {name: 'buy_id', index: 'buy_id', hidden: true},
                    {name: 'buy_name', index: 'buy_name', align: "center"},
                    {name: 'buy_spec', index: 'buy_spec', align: "center"},
                    {name: 'buy_num', index: 'buy_num', align: "center"},
                    {name: 'buy_price', index: 'buy_price', align: "center"},
                    {name: 'repair_worker_name', index: 'repair_worker_name', align: "center"},
                    {name: 'repair_num', index: 'repair_num', align: "center"},
                    {name: 'create_time', index: 'create_time', align: "center"}
                ],
                multiselect: false,
                ispaged: true,
                jsonReader: {
                    root: "d.data_list",
                    page: "d.page",
                    records: "d.total",
                    total: "d.max_page"
                }
            }, function () {});*/
        },
        methods: {
            /*reloadGrid: function() {
                var self = this;
                $("#grid").jqGrid('setGridParam', {
                    postData: {
                        'keyword': self.keyword
                    },
                    page: 1
                }).trigger("reloadGrid"); //重新载入
            },
            export: function() {
                var self = this;
                // 导出采购清单
                var elemIF = document.createElement("iframe");
                elemIF.src = '/api/repair/buy/export?keyword='+self.keyword;
                elemIF.style.display = "none";
                document.body.appendChild(elemIF);
            }*/
            showPersonalDiskFileFolder: function () {
                var self = this;
                layer.open({
								type: 1,
								area: ['500px', '400px'], //宽高
                                title:'移动到',
								content: $('#personalDiskPopupWindows'),
								cancel:function () {
									layer.closeAll();
								}
							})
            }
        }
    })
});