//初始化页面
var processRoute; // 全局变量，存储进程的运行路径；

$(function () {

    // 初始化用户已有主机地址
    var  hostObj=document.getElementById( 'host_ip' ); //根据id查找对象
    var url = "/input_process/get_host";
    $.getJSON(url, function (hosts)
    {
        for (var i=0; i<hosts.length;i++)
        {
            hostObj.add(new Option(hosts[i][0],hosts[i][1]));
        }
    });

    // 显示进程按钮功能
    $("#show").bind('click',function() {
        $("#show_process").html("").val("");  //清空原来信息
        // 获取当前下拉菜单中主机内容
        var hostObj=document.getElementById('host_ip');
        var index=hostObj.selectedIndex;  //序号，取当前选中选项的序号
        var hostIP = hostObj.options[index].text;  // 获取主机地址

        if (index == 0) alert("不合法主机地址");  // 警告选择不合法的主机地址
        var processValue = $("#process_value").val();  // 获取查询进程的信息

        // 获取在主机上查询的进程信息
        var showProcessObj=document.getElementById( 'show_process'); //根据id查找对象
        var url = "/input_process/get_process?host_ip="+hostIP+"&process_value="+processValue;
        var getDataFailure = $.getJSON(url, function (data)
        {
            var processStatus = data[0];
            processRoute = data[1]; // 路径的值
            showProcessObj.size = processStatus.length+1;  // 根据返回数据，大小可变
            for (var i=0; i<processStatus.length;i++)
            {
                showProcessObj.add(new Option(processStatus[i], i));
            }
        });
    });


    // 绑定保存按钮功能
    $("#save").bind('click',function() {
        var hostId = $("#host_ip").val(); //hostID值，注意
        var pid = $("#pid").val();
        if (pid=="") {
            alert("未发现监测的进程，请检查！");
            return
        }
        var shell = $("#shell").val();
        var cmd = $("#cmd").val();
        var time = $("#time").val();
        var logRoute = $("#log_route").val()+'/';
        var logName = $("#log_name").val();
        var codeRoute = $("#code_route").val()+'/';
        var codeName = $("#code_name").val();
        var comment = $("#comment").val();
        var url = "/input_process/save?host_id="+hostId+"&pid="+pid+"&shell="+shell+"&cmd="+cmd+"&time="+time+"&log_route="+logRoute+"&code_route="+codeRoute+"&code_name="+codeName+"&log_name="+logName+"&comment="+comment;
        $.getJSON(url, function (data)
        {

            if (data.result == "保存成功"){
                alert(data.result +'；进程号为：'+data.process_id);
                var hostObj=document.getElementById('host_ip');
                var index=hostObj.selectedIndex;  //序号，取当前选中选项的序号
                var hostIp = hostObj.options[index].text;  // 获取主机地址

                var url = "/process_details/execute_last?host_ip="+hostIp+"&pid="+pid+"&log_route="+logRoute+"&log_name="+logName+"&process_id="+data.process_id;
                $.getJSON(url, function (data)
                {
                    // alert(data.result)
                    reset();   //重置内容
                    return
                });
                reset();   //重置内容
            }
            else{
                alert(data.result)
            }

        });
    }); //保存按钮功能

     // 绑定重置按钮功能
    $("#reset").bind('click',function() {
        reset();
    }); //重置按钮功能

    // 鼠标移动到较长的input文本框，显示完整信息
    const inputElts = document.getElementsByTagName('input');
    Array.from(inputElts).map(elt => {
        elt.addEventListener('mouseenter', e => {
            const inputElt = e.target,
            font = window.getComputedStyle(inputElt)['font'];
            width = elt.clientWidth;
            if (inputElt.classList.contains('whole') && getTextWidth(inputElt.value, font) > width) {
                inputElt.title = inputElt.value;
            }
            else inputElt.title = '';
        })
    })
});

//获取文本框的宽度
function getTextWidth(text, font) {
    const canvas = getTextWidth.canvas || (getTextWidth.canvas = document.createElement('canvas')),
    context = canvas.getContext("2d");
    context.font = font;
    const metrics = context.measureText(text);
    return metrics.width;
}

// 清空重置
function reset() {
    // $("#pid").val('');
    $("#shell").val('');
    $("#cmd").val('');
    $("#log_route").val('');
    $("#log_name").val('');
    $("#code_route").val('');
    $("#code_name").val('');
    $("#comment").val('');
}

// 进程信息改变时事件
$("#show_process").change(function(){

    // 获取选择的进程信息
    var  processObj=document.getElementById('show_process');
    var  processIndex=processObj.selectedIndex;  //序号
    var  processInfo = processObj.options[processIndex].text;

    processInfo = processInfo.split(' '); // 分割为数组

    var pid = processInfo[0]; // 进程ID
    var shell  = processInfo[2];  // 执行程序
    var cmd = "";   // 运行命令
    var codeName = ""; // 运行文件名称
    var subProcessInfo = processInfo.slice(3,processInfo.length);
    // 得到运行命令和运行文件名称
    for (var i=0;i<subProcessInfo.length;i++)
    {
        var slice_value = subProcessInfo[i];
        cmd += ' ' + slice_value;
        if (-1 != slice_value.indexOf('.'))  codeName = subProcessInfo[i];
    }
    // 初始化进程基本信息
    $("#pid").val(pid);
    $("#shell").val(shell);
    $("#cmd").val(cmd);
    $("#code_name").val(codeName);
    $("#log_name").val('');  // 默认为空 ，可以提升优化为读取该运行文件下的所有文件，作为待选
    var pid_index = processRoute[0].indexOf(pid);  //得到进程的位置
    var route = processRoute[1][pid_index];  // 根据进程位置找到路径
    $("#log_route").val(route);
    $("#code_route").val(route);
    var hostObj=document.getElementById('host_ip');
    var index=hostObj.selectedIndex;  //序号，取当前选中选项的序号
    var hostIp = hostObj.options[index].text;

});