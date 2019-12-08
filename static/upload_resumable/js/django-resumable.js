var DjangoResumable = function (options) {
    "use strict";
    var defaults, els;
    if(options){
        options = this.extend(options, {});
    }else{
        options = options || {};
    }
    options = this.extend(options,{
        customCol: false
    });
    defaults = {
        //csrfInputName: 'csrfmiddlewaretoken',
        urlAttribute: 'data-upload-url',
        progressDisplay: 'inline',
        errorListClass: 'errorlist',
        onFilesLoaded: this.onFilesLoaded,
        onFileError: this.onFileError,
        onFileAdded: this.onFileAdded,
        onFileSuccess: this.onFileSuccess,
        onProgress: this.onProgress,
        resumable: null,
        view: {},
        resumableOptions: {},
        uploadHastrigged: false
    };
    this.options = this.extend(defaults, options);
    //this.csrfToken = document.querySelector('input[name=' + this.options.csrfInputName + ']').value;
    //静态部分
    var reUploadId = this.options.view.container.getAttribute('id');

    var h_str = '';
    if ( this.options.view.startBtn == true || this.options.view.addBtn == true ){
        h_str +=
            '<div class="upload-addfile-top" role="re-upload-show2">';
                h_str += '<span id="'+reUploadId+'_inp'+'_reUpload_fileNum" class="upload-file-number"></span>'
                        +'<span id="'+reUploadId+'_inp'+'_reUpload_fileNum2"></span>';
            if ( this.options.view.startBtn ){
                h_str += '<button class="btn-upload-start-upload">开始上传</button>';
            }
            if ( this.options.view.addBtn ){
                h_str += '<button class="btn-upload-addfile btn-1">添加文件</button>';
            }
        h_str += '</div>';
    }
    h_str +=
    '<form method="post" action="/api/upload/resumable" class="upload-form">'+
         '<button type="button" id="'+reUploadId+'_choose_localFile" class="choose-localFile-btn btn-medium btn-medium-upload" role="re-upload-show1">' +
            '本机选择文件</button>'+
         '<div class="upload-core-box" role="re-upload-show2">'+
            '<fieldset class="upload-fieldset">'+
                //'{% csrf_token %}'+
                '<label for="file-path" class="hidden"></label>'+
                '<input name="file-path" class="hidden">'+
                '<input id="'+reUploadId+'_inp" type="file" name="file" class="hidden" data-upload-url="/api/upload/resumable"  multiple="multiple" >'+
            '</fieldset>'+
        '</div>'+
    '</form>';
    h_str +=
        '<div class="upload-addfile-bottom" role="re-upload-show2">'+
            '<button class="btn-upload-confirm btn-2">确认</button>'+
            '<button class="btn-upload-cancel btn-2">取消</button>'+
        '</div>';
    if ( this.options.view.dragable == true ){
        h_str +=
            '<div class="drag-info" role="re-upload-show1">'+
                '<div class="tip-info drag-box">将文件拖拽至此处...</div>'+
                '<div class="tip-info-2">或</div>'+
            '</div>';
    }

    var container = this.options.view.container ;
    container.innerHTML = h_str;
    var btn = document.getElementById(reUploadId+'_choose_localFile');
    btn.addEventListener('click', function (e) {
        document.getElementById(reUploadId+'_inp').click();
    });
    els = document.querySelectorAll('input[' + this.options.urlAttribute + ']');
    this.each(els, function (el) {
        this.initField(el);
    });

    //bind confirm  cancel buttons
    var self = this;
    if (typeof( self.options.xhrfile.confirm) == 'function'){
        var btn_confirm = container.getElementsByClassName('btn-upload-confirm');
        self.each(btn_confirm,function(el){
            el.addEventListener('click', function (e) {
                var waitNumber = 0, errorNumber = 0;
                var tbody = document.getElementById(reUploadId+'_inp-table-body');
                var tds = tbody.querySelectorAll('td[for="resum_fileStatus"]');
                self.each(tds, function (td) {
                    if (td.innerHTML == '等待上传'){
                        waitNumber = waitNumber+1;
                    }else if (td.innerHTML == '上传失败'){
                        errorNumber = errorNumber+1;
                    }
                });
                if (waitNumber>0){
                    document.getElementById( reUploadId+'_inp'+'_reUpload_fileNum2').innerHTML = '&nbsp;&nbsp;'
                        + '<font color="red">还有'+waitNumber+'个未上传文件</font>';
                    setTimeout(function () {
                        document.getElementById( reUploadId+'_inp'+'_reUpload_fileNum2').innerHTML = '';
                    },3000);
                    return;
                }
                if (self.options.resumable.files.length == 0){
                    self.options.xhrfile.confirm.apply(self,[self.options.resumable.files]);
                    return;
                }
                if (self.options.resumable.files[self.options.resumable.files.length - 1].isComplete() == false){
                    document.getElementById( reUploadId+'_inp'+'_reUpload_fileNum2').innerHTML = '&nbsp;&nbsp;'
                        + '<font color="red">还有1个文件正在上传</font>';
                    setTimeout(function () {
                        document.getElementById( reUploadId+'_inp'+'_reUpload_fileNum2').innerHTML = '';
                    },3000);
                    return;
                }
                self.options.xhrfile.confirm.apply(self,[self.options.resumable.files]);
            });
        });
    }
    if (typeof( self.options.xhrfile.cancel) == 'function'){
        var btn_cancel = container.getElementsByClassName('btn-upload-cancel');
        self.each(btn_cancel,function(el){
            el.addEventListener('click', function (e) {
                self.options.xhrfile.cancel.apply(self,[]);
            });
        });
    }
    return (this);
};

DjangoResumable.prototype.remove = function () {
    //销毁 form progressBar_box, table， ect;
    var els = document.querySelectorAll('input[' + this.options.urlAttribute + ']');
    this.each(els, function (el) {
        this.removeField(el);
    });
    //销毁 resumable
    var r = this.options.resumable;
    r.removeAllFile();
};


DjangoResumable.prototype.each = function (elements, fn) {
    "use strict";
    var i, l;
    for (i = 0, l = elements.length; i < l; i += 1) {
        fn.apply(this, [elements[i]]);
    }
};


DjangoResumable.prototype.extend = function (target, source) {
    "use strict";
    var property;
    for (property in source) {
        if (source.hasOwnProperty(property)) {
            target[property] = source[property];
        }
    }
    return target;
};


DjangoResumable.prototype.fileTypeErrorCallback = function (file, errorCount) {
    "use strict";
    layer.msg(file.fileName||file.name +'文件类型错误，请选择' + this.fileType.join(',') + '文件');
};


DjangoResumable.prototype.maxFilesErrorCallback = function (file, errorCount) {
    "use strict";
    layer.msg('请不要超过'+this.maxFiles+'个文件');
};


DjangoResumable.prototype.getErrorList = function (el, create) {
    "use strict";
    var errorList = el.parentNode.previousSibling;
    while (errorList && errorList.tagName === undefined) {
        errorList = errorList.previousSibling;
    }
    if (errorList && !errorList.classList.contains(this.options.errorListClass)) {
        if (create === true) {
            errorList = document.createElement('ul');
            errorList.classList.add(this.options.errorListClass);
            el.parentNode.parentNode.insertBefore(errorList, el.parentNode);
        } else {
            errorList = null;
        }
    }
    return errorList;
};


DjangoResumable.prototype.getForm = function (el) {
    "use strict";
    var parent = el;
    while (parent.tagName !== 'FORM') {
        parent = parent.parentNode;
    }
    return parent;
};


DjangoResumable.prototype.formatBytes = function (bytes) {
    "use strict";
    if      (bytes>=1073741824) {bytes=(bytes/1073741824).toFixed(2)+' GB';}
    else if (bytes>=1048576)    {bytes=(bytes/1048576).toFixed(2)+' MB';}
    else if (bytes>=1024)       {bytes=(bytes/1024).toFixed(2)+' KB';}
    else if (bytes>1)           {bytes=bytes+' bytes';}
    else if (bytes==1)          {bytes=bytes+' byte';}
    else                        {bytes='0 byte';}
    return bytes;
};


DjangoResumable.prototype.initField = function (el) {
    "use strict";
    var progressBar_box, progress, table, fileName, filePath, filePathName;
    progress = this.initProgressBar(el);
    progressBar_box = this.initProgressBar_box(el);
    progressBar_box.insertBefore(progress ,progressBar_box.lastChild);
    table = this.initFilesTable(el);
    //el.parentNode.insertBefore(progress, el.nextSibling);

    el.parentNode.insertBefore(progressBar_box, el.nextSibling);
    el.parentNode.insertBefore(table, progressBar_box.nextSibling);

    filePathName = el.getAttribute('name') + '-path';
    filePath = el.parentNode.querySelector('[name=' + filePathName + ']');
    fileName = el.parentNode.querySelector('label[for=' + filePathName + ']');

    this.initResumable(el, progress, filePath, fileName);

    this.getForm(el).addEventListener('submit', function () {
        el.parentNode.removeChild(el);
    });
};

DjangoResumable.prototype.removeField = function (el) {
    "use strict";
    var reUploadId = el.getAttribute('id');
    var progressBar_box, table;
    progressBar_box = document.getElementById( reUploadId + '-progressBar');
    table = document.getElementById( reUploadId + '-table');
    el.parentNode.removeChild(progressBar_box);
    el.parentNode.removeChild(table);
};

DjangoResumable.prototype.initProgressBar = function (el) {
    "use strict";
    var reUploadId = el.getAttribute('id');
    var progress = document.createElement('progress');
    progress.setAttribute('id', reUploadId + '-progress');
    progress.setAttribute('value', '0');
    progress.setAttribute('max', '1');
    progress.setAttribute('class','re-progress');
    //progress.style.display = 'none';
    return progress;
};


DjangoResumable.prototype.initProgressBar_box = function (el) {
    "use strict";
    var reUploadId = el.getAttribute('id');
    var progressBar_box,percent;
    percent = document.createElement('label');
    percent.setAttribute('for', reUploadId+ '-progress');
    percent.setAttribute('class','re-percent');
    percent.innerHTML = '0%';
    progressBar_box = document.createElement('div');
    progressBar_box.setAttribute('id', reUploadId + '-progressBar');
    progressBar_box.setAttribute('class','re-progress-box');
    progressBar_box.appendChild(percent);
    return progressBar_box;
};


DjangoResumable.prototype.initFilesTable = function (el) {
    "use strict";
    var custom_td='';
    if (this.options.view.colNames && this.options.view.colNames.length>0){
        this.options.customCol = true;
        var colNames = this.options.view.colNames;
        var colModel = this.options.view.colModel;
        for (var i=0; i<colNames.length; i++){
            custom_td += '<td name="'+colModel[i].name+'" class="re-td" style="width:72px;" >'+colNames[i]+'</td>'
        }
    }
    "use strict";
    var reUploadId = el.getAttribute('id');
    var table = document.createElement('table');
    table.setAttribute('id',reUploadId + '-table');
    table.setAttribute('class','re-table');
    var table_html = '<thead>' +
        '<td name="resum_fileId" class="re-td" style="display:none;">文件ID</td>' +
        '<td name="resum_fileName" class="re-td" width="40%">文件名</td>' +
        '<td name="resum_fileSize" class="re-td" width="15%">大小</td>' +
        '<td name="resum_fileStatus" class="re-td" width="30%">状态</td>' +
        '<td name="resum_fileOper" class="re-td" width="15%">操作</td>' +
            custom_td +
        '<td name="s3_fileId" style="display:none;">s3_文件ID</td>' +
        '<td name="s3_fileName" style="display:none;">s3_文件名</td>' +
        '<td name="s3_fileSize" style="display:none;">s3_文件大小</td>' +
        '<td name="s3_fileType" style="display:none;">s3_文件类型</td>' +
        '<td name="s3_fileUrl" style="display:none;">s3_文件URL</td>' +
        '</thead>';
        table_html += '<tbody id="'+ reUploadId +'-table-body"></tbody>';
    table.innerHTML = table_html;
    return table;
};



DjangoResumable.prototype.initResumable = function (el, progress, filePath, fileName) {
    "use strict";
    var elements = Array.prototype.slice.call(arguments),
        self = this,
        opts = {
            target: el.getAttribute(this.options.urlAttribute),
            query: {
                //'csrfmiddlewaretoken': this.csrfToken,
            }
        };
    if ( this.options.resumableOptions.maxFiles ){
        this.maxFiles = parseInt( this.options.resumableOptions.maxFiles );
        this.options.resumableOptions['maxFilesErrorCallback'] = this.maxFilesErrorCallback;
    }
    if ( this.options.resumableOptions.fileType ){
        this.fileType = this.options.resumableOptions.fileType;
        this.options.resumableOptions['fileTypeErrorCallback'] = this.fileTypeErrorCallback;
    }

    opts = this.extend(this.options.resumableOptions, opts);
    var r = new Resumable(opts);
    this.options.resumable = r;
    r.assignBrowse(el);
    if (this.options.view.dragable == true){
        var container = this.options.view.container;
        var box = container.getElementsByClassName('drag-box');
        r.assignDrop(box);
    }
    if (this.options.view.addBtn == true){
        var container = this.options.view.container;
        var button = container.getElementsByClassName('btn-upload-addfile');
        r.assignBrowse(button);
    }
    this.each(['filesLoaded', 'fileAdded', 'progress', 'fileSuccess', 'fileError'], function (eventType) {
        var callback = this.options['on' + eventType.substring(0, 1).toUpperCase() + eventType.substring(1)];
        r.on(eventType, function () {
            var args = arguments.length > 0 ? Array.prototype.slice.call(arguments) : [];
            callback.apply(self, [r].concat(args).concat(elements));
        });
    });
    return r;
};


DjangoResumable.prototype.onFilesLoaded = function (r, files, el, progress) {
    "use strict";
    var self = this;
    var reUploadId = el.getAttribute('id');
    document.getElementById(reUploadId+'-table').style.display = 'table';
    var container = this.options.view.container,
        els1 = container.querySelectorAll('[role="re-upload-show1"]'),
        els2 = container.querySelectorAll('[role="re-upload-show2"]');
    this.each(els1, function (el) {
        el.style.display = 'none';
    });
    this.each(els2, function (el) {
        el.style.display = 'block';
    });
    if (typeof(this.options.xhrfile.loaded) == 'function'){
        this.options.xhrfile.loaded.apply(this);
    }
    //是否手动上传
    var clickFileInput = function () {
        //等待上传的个数 > 1
        var waitNumber = 0;
        var tbody = document.getElementById(reUploadId+'-table-body');
        var tds = tbody.querySelectorAll('td[for="resum_fileStatus"]');
        self.each(tds, function (td) {
            if (td.innerHTML == '等待上传'){
                waitNumber = waitNumber+1;
            }
        });
        if (waitNumber >= 1){
            self.fileStart(r);
        }
    };
    if (this.options.view.startBtn){
        var buttons = container.getElementsByClassName('btn-upload-start-upload');
        this.each(buttons,function(el){
            el.removeEventListener('click', clickFileInput);
            el.addEventListener('click', clickFileInput);
        });
    }else{
        setTimeout(function () {
            self.fileStart(r);
        },10);
    }
};

DjangoResumable.prototype.filesRemove = function () {
    this.options.uploadHastrigged = false;
    this.options.resumable.removeAllFile();
    var reUploadId = this.options.view.container.getAttribute('id');
    document.getElementById(reUploadId + '_inp-table-body').innerHTML = '';
    document.getElementById(reUploadId + '_inp_reUpload_fileNum').innerHTML = '已添加0个文件';
};


DjangoResumable.prototype.fileStart = function (r) {
    "use strict";
    var self = this;
    var start = true;
    if (typeof(this.options.xhrfile.beforeStart) == 'function'){
        start = this.options.xhrfile.beforeStart.apply(this);
    }
    if (start){
        if (r.isUploading()) return;
        if ( !this.options.uploadHastrigged ){
            this.options['uploadHastrigged'] = true;
            r.upload(); // TODO 多次调用 ，存在并发的问题。 观察，每次点击 添加文件之后，都会多触发一次 。在progress == 1时，禁用掉添加文件。
        }
        if (typeof(this.options.xhrfile.start) == 'function'){
            this.options.xhrfile.start.apply(self);
        }
    }
}

DjangoResumable.prototype.onFileError = function (r, file, message, el) {
    "use strict";
    var rowDOM = document.getElementById(file.uniqueIdentifier);
    rowDOM.querySelector('td[for="resum_fileStatus"]').innerHTML = '上传失败';
    rowDOM.querySelector('td[for="resum_fileStatus"]').setAttribute('class','re-td error')
};


DjangoResumable.prototype.onFileAdded = function (r, file, event, el, progress, filePath, fileName) {
    var container = this.options.view.container,
        els1 = container.querySelectorAll('[role="re-upload-show1"]'),
        els2 = container.querySelectorAll('[role="re-upload-show2"]');
    this.each(els1, function (el) {
        el.style.display = 'none';
    });
    this.each(els2, function (el) {
        el.style.display = 'block';
    });
    "use strict";
    var self = this;
    var this_r = r;
    var this_file = file;
    var reUploadId = el.getAttribute('id');
    var tbody = document.getElementById(reUploadId+'-table-body');
    //判断 tr 的行数，是否超出 maxFiles
    if ( self.maxFiles > 1 ){
        var trs = tbody.querySelectorAll('tr');
        if ( trs.length+1 > self.maxFiles){
            layer.msg('请不要超过'+self.maxFiles+'个文件');
            return;
        }
    }else if ( self.maxFiles == 1 ){
        var trs = tbody.querySelectorAll('tr');
        if ( trs.length > 0){
            tbody.innerHTML = '';
            document.getElementById(reUploadId +'_reUpload_fileNum').innerHTML = '已添加0个文件';
        }
    }
    /**文件列表**/
    var tr=document.createElement('tr');
    tbody.appendChild(tr);
    tr.setAttribute('id',file.uniqueIdentifier);
    tr.setAttribute('class','re-tr');
    tr.innerHTML +=
        '<td for="resum_fileId" class="re-td" style="display:none;"></td>'+
        '<td for="resum_fileName" class="re-td">'+file.fileName+'</td>'+
        '<td for="resum_fileSize" class="re-td">'+ this.formatBytes(file.size)+'</td>'+
        '<td for="resum_fileStatus" class="re-td">等待上传</td>'+
        '<td for="resum_fileOper" class="re-td"><span class="oper-del">删除</span></td>'+
            //other_td +
        '<td for="s3_fileId" style="display:none;"></td>' +
        '<td for="s3_fileName" style="display:none;"></td>' +
        '<td for="s3_fileSize" style="display:none;"></td>' +
        '<td for="s3_fileType" style="display:none;"></td>' +
        '<td for="s3_fileUrl" style="display:none;"></td>';
    var span = document.getElementById(reUploadId +'_reUpload_fileNum');
    span.innerHTML = '已添加'+ r.files.length +'个文件';
    var other_td = '';
    if (this.options.customCol){
        var colModel = this.options.view.colModel;
        for (var i=0; i<colModel.length; i++){
            var td = document.createElement('td');
            td.setAttribute('for',colModel[i].name);
            td.setAttribute('class','re-td');
            if (this.options.view.colModel[i].formatter && typeof (this.options.view.colModel[i].formatter)=='function'){
                td.innerHTML = this.options.view.colModel[i].formatter.apply(self,[tr])
            }
            tr.insertBefore(td, tr.querySelector('td[for="s3_fileId"]'))
        }
    }
    //bind
    var _td =  tr.querySelector('td[for="resum_fileOper"]');
    var _span = _td.querySelector('span.oper-del');
    _span.removeEventListener('click',delThisFile);
    _span.addEventListener('click',delThisFile);
    function delThisFile(){
        var fileObj = {
            id: tr.querySelector('td[for="s3_fileId"]').innerHTML,
            name: tr.querySelector('td[for="s3_fileName"]').innerHTML,
            size: tr.querySelector('td[for="s3_fileSize"]').innerHTML,
            type: tr.querySelector('td[for="s3_fileType"]').innerHTML,
            url: tr.querySelector('td[for="s3_fileUrl"]').innerHTML
        };
        r.removeFile(file);
        var span = document.getElementById(reUploadId +'_reUpload_fileNum');
        span.innerHTML = '已添加'+ r.files.length +'个文件';
        var _parentElement = tr.parentNode;
        if(_parentElement){
            _parentElement.removeChild(tr);
        }
        if (typeof(self.options.xhrfile.remove) == 'function'){
            self.options.xhrfile.remove.apply(self,[fileObj]);
        }
    }
};


DjangoResumable.prototype.onFileSuccess = function (r, file, message, el, progress, filePath, fileName) {
    "use strict";
    var self = this;
    filePath.setAttribute('value', file.size + '_' + file.fileName);
    var row = document.getElementById(file.uniqueIdentifier);
    var data = JSON.parse(message);
    if (data.c == 0){
        row.querySelector('td[for="resum_fileStatus"]').innerHTML = '上传完成';
        row.querySelector('td[for="resum_fileStatus"]').setAttribute('class','re-td success');
        row.querySelector('td[for="resum_fileOper"]').innerHTML = '<span class="oper-del disabled">删除</span>';
        row.querySelector('td[for="s3_fileId"]').innerHTML = data.d[0].id;
        row.querySelector('td[for="s3_fileName"]').innerHTML = data.d[0].name;
        row.querySelector('td[for="s3_fileSize"]').innerHTML = data.d[0].size;
        row.querySelector('td[for="s3_fileType"]').innerHTML = data.d[0].type;
        row.querySelector('td[for="s3_fileUrl"]').innerHTML = data.d[0].url;
    }
    if (typeof(this.options.xhrfile.success)=='function'){
        this.options.xhrfile.success.apply(self,[data]);
    }

};


DjangoResumable.prototype.onProgress = function (r, el, progress, filePath, fileName) {
    "use strict";
    var self = this;
    progress.setAttribute('value', r.progress());
    var all_percent = progress.parentNode.querySelector('label[for=' + progress.getAttribute('id') + ']');
    var pos ='';
    if (r.progress()==0 || r.progress()==1){
        pos = (r.progress()*100).toFixed(0) + '%';　
    }else{
        pos = (r.progress()*100).toFixed(2) + '%';
    }　
    all_percent.style.left = pos;
    all_percent.innerHTML = pos;
    for (var i=0; i< r.files.length; i++){
        var tmp_file = r.files[i];
        var row = document.getElementById( tmp_file.uniqueIdentifier);
        if (tmp_file._prevProgress > 0 && tmp_file._prevProgress <1){
            row.querySelector('td[for="resum_fileOper"]').innerHTML = '<span class="oper-del disabled">删除</span>';
            var _pro = tmp_file.progress();
            if (_pro==0 || _pro==1){
                _pro = (_pro*100).toFixed(0) + '%';　
            }else{
                _pro = (_pro*100).toFixed(2) + '%';
            }
            var id = tmp_file.uniqueIdentifier;
            var progressBar = document.createElement('div');
                progressBar.setAttribute('id',id+'-progressBar');
                progressBar.setAttribute('class','re-progress-box');
                progressBar.setAttribute('style','display: inline-block;');
            var progress = document.createElement('progress');
                progress.setAttribute('id',id+'-progress');
                progress.setAttribute('value',tmp_file.progress());
                progress.setAttribute('max',1);
                progress.setAttribute('class','re-progress');
                progress.setAttribute('style','display:inline');
            var label = document.createElement('label');
                label.setAttribute('for',id+'-progress');
                label.setAttribute('class','re-percent');
                label.style.left = _pro;
                label.innerHTML = _pro;
            progressBar.appendChild(progress);
            progressBar.appendChild(label);
            row.querySelector('td[for="resum_fileStatus"]').innerHTML = '';
            row.querySelector('td[for="resum_fileStatus"]').appendChild(progressBar);
        }
    }
    if (r.progress() == 1){
        //禁用
        this.options.uploadHastrigged = false;
    }
    if (typeof(this.options.xhrfile.progress)=='function'){
        this.options.xhrfile.progress.apply(self, [r.progress()]);
    }
};
