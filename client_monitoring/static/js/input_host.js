//初始化页面
$(function () {
    // 绑定测试按钮功能
    $("#test").bind('click',function() {
        var hostIp = $("#host_ip").val();
        var port = $("#port").val();
        if (port == ""){
            port = 22;  // 默认端口号为22
        }
        var loginName = $("#login_name").val();
        var pwd = $("#pwd").val();
        // 验证输入信息是否合法
        if (checkValidity(hostIp,port,loginName,pwd))
        {
            var url = "/input_host/test?host_ip="+hostIp+"&port="+port+"&login_name="+loginName+"&pwd="+pwd;
            $.getJSON(url, function (data)
            {
                alert(data.result);
            });
        }
    }); //测试连接功能

    // 绑定保存按钮功能

    $("#save").bind('click',function() {
        var hostIp = $("#host_ip").val();
        var port = $("#port").val();
        if (port == ""){
            port = 22;  // 默认端口号为22
        }
        var loginName = $("#login_name").val();
        var pwd = $("#pwd").val();
        var comment = $("#comment").val();
        if (checkValidity(hostIp,port,loginName,pwd))
        {
            var url = "/input_host/save?host_ip="+hostIp+"&port="+port+"&login_name="+loginName+"&pwd="+pwd+"&comment="+comment;
            $.getJSON(url, function (data)
            {
                alert(data.result);
                reset();
            });
        }
    }); //保存按钮功能
});

function reset() {

     $("#host_ip").val('');
     $("#port").val('');
     $("#login_name").val('');
     $("#pwd").val('');
     $("#comment").val('');
}


// 验证用户输入内容是否合法
function checkValidity(host_ip,port,login_name,pwd) {
    if (host_ip==""  || login_name=="" || pwd=="" )
    {
        alert("所填信息不能为空");
        return false
    }
    if (!checkIP(host_ip)){
        alert("填写合法IP");
        return false
    }
    if(isNaN(port))
    {
        alert("端口号必须为数字");
        return false
    }
    return true
}

// 验证IP地址是否合法
function checkIP(ip)
{
   var re=/^(\d+)\.(\d+)\.(\d+)\.(\d+)$/;//正则表达式
   if(re.test(ip))
   {
       if( RegExp.$1<256 && RegExp.$2<256 && RegExp.$3<256 && RegExp.$4<256)
       return true;
   }
   return false;
}



