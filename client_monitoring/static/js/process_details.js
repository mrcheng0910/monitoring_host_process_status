var gloable_process_id; // 全局变量

function setCookie(cname,cvalue,exdays)
{
  var d = new Date();
  d.setTime(d.getTime()+(exdays*24*60*60*1000));
  var expires = "expires="+d.toGMTString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}


$(function () {

    //按钮绑定最新动态功能
    $("#update").bind('click',function() {

        var hostIp = $("#host_ip").val();
        var log_route = $("#process_log_route").val();
        var log_name = $("#log_name").val();
        var pid = $("#pid").val();

        var url = "/process_details/execute_last?host_ip="+hostIp+"&pid="+pid+"&log_route="+log_route+"&log_name="+log_name+"&process_id="+gloable_process_id;
        $.getJSON(url, function (data)
        {
            alert(data.result);
            location.reload();
        });
    });

    // 绑定杀死按钮功能
    $("#stop").bind('click',function() {

        var hostIp = $("#host_ip").val();
        var pid = $("#pid").val();
        var url = "/process_details/stop?host_ip="+hostIp+"&pid="+pid;
        $.getJSON(url, function (data)
        {

            if (data.result=="停止成功"){  // 停止成功后，运行一次，更新页面
                $("#update").click();
            }else {
                alert(data.result);
            }

        });
    });

    // 绑定取消按钮功能
    $("#nofocus").bind('click',function() {
        var url = "/process_details/nofocus?process_id="+gloable_process_id;
        $.getJSON(url, function (data)
        {
            alert(data.result);
            location.replace('/');
        });
    });

    // 绑定重新执行进程按钮功能
    $("#run").bind('click',function() {

        var hostIp = $("#host_ip").val();
        var logRoute = $("#process_log_route").val();
        var logName = $("#log_name").val();
        var shell = $("#shell").val();
        var cmd = $("#cmd").val();
        var codeRoute = $("#code_route").val();
        var codeName = $("#code_name").val();
        var comment = $("#comment").val();
        var interval_time = $("#interval_time").val();
        var url = "/process_details/execute_process?code_route="+codeRoute+"&code_name="+codeName+"&log_route="+logRoute+"&log_name="+logName+"&shell="+shell+"&cmd="+cmd+"&process_id="+gloable_process_id+"&host_ip="+hostIp+"&comment="+comment+"&interval_time="+interval_time;

         $.getJSON(url, function (data)
        {
            if (data.result == "执行失败"){
                alert(data.result);
            }
            else {
                var url = "/process_details/execute_last?host_ip="+hostIp+"&pid="+data.result+"&log_route="+logRoute+"&log_name="+logName+"&process_id="+gloable_process_id;
                $.getJSON(url, function (data)
                {
                    alert(data.result);
                    location.reload();
                });
            }
        });
    });

    // 绑定查看日志按钮功能
    $("#check_log").bind('click',function() {

        var hostIp = $("#host_ip").val();
        var log_route = $("#process_log_route").val();
        var log_name = $("#log_name").val();
        var url = "/process_details/read_log?host_ip="+hostIp+"&log_route="+log_route+"&log_name="+log_name;
        $.getJSON(url, function (data)
        {
            $("#test").val(data.result);
        });
    });

    // 绑定下载日志功能
    $("#download_log").bind('click',function() {

        var hostIp = $("#host_ip").val();
        var log_route = $("#process_log_route").val();
        var log_name = $("#log_name").val();
        var data_url = "/process_details/download_log?host_ip="+hostIp+"&log_route="+log_route+"&log_name="+log_name;
        location.href = data_url;  // 待优化，未对异常进行处理
    });


    //按钮绑定编辑进程信息按钮
    $("#edit_process").bind('click',function() {
        $("#log_route_modal").val($("#process_log_route").val());
        $("#log_name_modal").val($("#log_name").val());
        $("#code_name_modal").val($("#code_name").val());
        $("#code_route_modal").val($("#code_route").val());
        $("#shell_modal").val($("#shell").val());
        $("#cmd_modal").val($("#cmd").val());
        $("#interval_time_modal").val($("#interval_time").val());
        $("#comment_modal").val($("#comment").val());
        $("#warning_times_modal").val($("#warning_times").val());

    });

    //按钮绑定提交编辑进程信息功能
    $("#submit_edit_process").bind('click',function() {
        var logRoute = $("#log_route_modal").val();
        var logName = $("#log_name_modal").val();
        var codeName = $("#code_name_modal").val();
        var codeRoute = $("#code_route_modal").val();
        var shell = $("#shell_modal").val();
        var cmd = $("#cmd_modal").val();
        var interalTime = $("#interval_time_modal").val();
        var comment = $("#comment_modal").val();
        var warningTimes = $("#warning_times_modal").val();
        var url = "/process_details/submit_process?code_route="+codeRoute+"&code_name="+codeName+"&log_route="+logRoute+"&log_name="+logName+"&shell="+shell+"&cmd="+cmd+"&process_id="+gloable_process_id+"&interval_time="+interalTime+"&comment="+comment+"&warning_times="+warningTimes;
        $.getJSON(url, function (data)
        {
            alert(data.result);
            // $('#process_modal').modal('hide');
            location.reload();  //刷新
        });
    });
});

// 对探测间隔时长输入进行监测
function intervalTimeRequire(){
    var interval_time = $("#interval_time_modal").val();
    if (interval_time<15){
        alert("探测间隔时间最短为15分钟");
        $("#interval_time_modal").val(15);  // 重置为15分钟
    }
}


// 显示进程详细信息
function showProcessDetails(process_id){
    gloable_process_id = process_id;
    $.ajax({
        url: '/process_details/data',
        type: "get",
        data: {
            process_id: process_id,
            stamp: Math.random()
        },
        timeout: 1200, //超时时间
        success: function (data) {  //成功后的处理


            var rawData = JSON.parse(data); //json格式化原始数据
            showCurrentStatus(rawData[0]);
            showTimeline(rawData[1],'%','CPU占用百分比',"#container_cpu"); //CPU占用情况百分比
            showTimeline(rawData[2],'%','内存占用百分比',"#container_mem"); //内存占用百分比
            showTimeline(rawData[3],'M','虚拟内存',"#container_vsz"); //虚拟内存
            showTimeline(rawData[4],'M','内存',"#container_rss"); //内存
            showTimeline(rawData[5],'M','日志大小',"#container_log"); //日志
        },
        error: function (xhr) {
            if (xhr.status == "0") {
                alert("超时，稍后重试");
            } else {
                alert("错误提示：" + xhr.status + " " + xhr.statusText);
            }
        } // 出错后的处理
    });
}

// 显示进程最新状态信息
function showCurrentStatus(current_status) {

    var s1 = new Date(current_status.detect_time);
    var s2 = new Date(current_status.create_time);
    $("#host_ip").attr("value",current_status.host_ip);
    var status = $("#process_status").attr("value",current_status.status);
    $("#process_name").attr("value",current_status.process_name);
    $("#pid").attr("value",current_status.pid);
    $("#process_create").attr("value",current_status.create_time);
    $("#process_detect").attr("value",current_status.detect_time);
    $("#process_long").attr("value",((s1-s2)/3600000).toFixed(0));  // 小时
    $("#process_error").attr("value",current_status.error_info);
    $("#process_log_route").attr("value",current_status.log_route);
    $("#log_name").attr("value",current_status.log_name);
    $("#code_route").attr("value",current_status.code_route);
    $("#code_name").attr("value",current_status.process_name);
    $("#shell").attr("value",current_status.shell);
    $("#cmd").attr("value",current_status.cmd);
    $("#comment").attr("value",current_status.comment);
    $("#interval_time").attr("value",current_status.interval_time);
    $("#warning_times").attr("value",current_status.warning_times);

    // 设置按钮的状态，防止用户误操作
    if (current_status.status == '正常') {
        $("#run").attr('disabled', true);  // 状态正常时，则其运行进程功能禁止
    }else if (current_status.status == "停止"){   // 停止状态时，部分按钮失效和部分框可输入
        $("#update").attr('disabled', true);
        $("#stop").attr('disabled', true);
        $("#edit_process").attr('disabled',true);
         $("#process_log_route").attr("readonly",false);
         $("#shell").attr("readonly",false);
         $("#cmd").attr("readonly",false);
         $("#code_name").attr("readonly",false);
         $("#interval_time").attr("readonly",false);
         $("#comment").attr("readonly",false);
         $("#log_name").attr("readonly",false);
         $("#code_route").attr("readonly",false);
         $("#shuoming").attr("hidden",false);

    }else if(current_status.status == "异常"){
        $("#run").attr('disabled', true);
    }

    // 日志文件名称为空，则查看日志功能失效
    if (current_status.log_name == ""){
        $("#check_log").attr('disabled', true);
        $("#download_log").attr('disabled', true);
    }

}


function  showTimeline(data,suffix,series_name,tag_name) {

    var cat = [];
    var d = [];
    for (var i=0;i<data.length;i++){
        cat.push(data[i][0]);
        d.push(data[i][1])
    }
    var title = {
      text: null
   };
   var xAxis = {
      categories: cat
   };
   var yAxis = {
      title: {
         text: '占用情况'
      },
      plotLines: [{
         value: 0,
         width: 1,
         color: '#808080'
      }]
   };

   var tooltip = {
      valueSuffix: suffix
   };

   var legend = {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'middle',
      borderWidth: 0
   };

   var series =  [
      {
         name: series_name,
         data: data
      }

   ];

   var json = {};

   json.title = title;
   json.xAxis = xAxis;
   json.yAxis = yAxis;
   json.tooltip = tooltip;
   json.legend = legend;
   json.series = series;
   $(tag_name).highcharts(json);
}

