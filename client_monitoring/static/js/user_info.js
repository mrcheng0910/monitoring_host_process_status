//初始化页面
$(function () {

    if($("#user_type").val()=="普通用户"){
         $("#add_user").hide();
    }

    // 按钮绑定修改用户信息功能
    $("#edit_info").bind('click',function() {
        $("#user_name").attr("readonly",false);
        $("#email").attr("readonly",false);
        $("#save").show();
	    $('#edit').attr('disabled',"true");
    });

    // 按钮绑定保存用户信息功能
    $("#save").bind('click',function() {

        var userName = $("#user_name").val();
        var email = $("#email").val();
        var url = "/user/edit_user?user_name="+userName+"&email="+email;
        $.getJSON(url, function (data)
        {
            alert(data.result);
            // setCookie('username',userName,30);
            location.reload();
        });
    });
    // 修改密码功能
    $("#edit").bind('click',function() {
        $("#edit_pwd").show();
        $('#edit_info').attr('disabled',"true");
        $("#save_edit_pwd").show();

    });

    $("#save_edit_pwd").bind('click',function() {
        var old_pwd = $("#old_pwd").val();
        var new_pwd = $("#new_pwd").val();
        var confirm_pwd = $("#confirm_pwd").val();

        if (new_pwd != confirm_pwd) {
            alert("新密码不一致");
        }
        else if(new_pwd=="") {

            alert("新密码不能为空");
        }
        else {

            var url = "/user/edit_user_pwd?old_pwd="+old_pwd+"&new_pwd="+new_pwd;
            $.getJSON(url, function (data)
            {
                alert(data.result);
                location.reload();
            });
        }
    });

    $("#add_user").bind('click',function() {
        $("#new_user").show();
        $("#add_user").hide();
    });

    $("#save_new_user").bind('click',function() {

        var userName = $("#new_user_name").val();
        var loginName = $("#new_user_login_name").val();
        var newUserPwd = $("#new_user_pwd").val();
        var newUserConPwd = $("#new_user_confirm_pwd").val();
        var newType = $("#new_user_type").val();
        var newEmail = $("#new_user_email").val();

        if (userName == "" || loginName=="" || newEmail==""){
            alert("信息不能为空");
            return
        }

        if (newUserPwd != newUserConPwd){
            alert("密码不一致");
        }else if(newUserPwd==""){
            alert("密码不能为空");
        }else
            {
            var url = "/user/add_user?user_name="+userName+"&login_name="+loginName+"&pwd="+newUserPwd+"&flag="+newType+"&email="+newEmail;
            $.getJSON(url, function (data)
            {
                alert(data.result);
                location.reload();
            });
        }
    });

});

