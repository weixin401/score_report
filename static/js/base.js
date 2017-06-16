/**
 * Created by root on 17-6-7.
 */
$(document).ready(function(){

    var $el = $('.dialog');
    $el.hDialog(); //默认调用

    //页面加载完成后自动执行
    $('#autoShow').hDialog({title:'页面加载完成后自动执行',autoShow: true});

    //带标题的
    $('.demo0').hDialog({title: '测试弹框标题',height: 300});

    //改变宽度
    $('.demo1').hDialog({width: 500});

    //改变高度
    $('.demo2').hDialog({height: 400});

    //改变宽和高
    $('.demo3').hDialog({width:600,height: 500});

    //改变位置
    $('.demo4').hDialog({positions: 'bottom',effect: 'slideOutDown'});

    //不清空表单
    $('.demo5').hDialog({resetForm: false});

    //遮罩不可关闭
    $('.demo6').hDialog({modalHide: false});

    //改变弹框背景色
    $('.demo7').hDialog({boxBg: '#eeeeee'});

    //改变遮罩背景色
    $('.demo8').hDialog({modalBg: 'rgba(255,255,255,0.7)'});

    //改变关闭背景色
    $('.demo9').hDialog({closeBg: '#4A74B5'});

    //错误文字提示
    $('.demo10').click(function(){
        $.tooltip('My God, 出错啦！！！');
    });

    //正确文字提示
    $('.demo11').click(function(){
        $.tooltip('OK, 操作成功！', 2500, true);
    });

    //显示加载
    $('.demo12').click(function(){
        //自定义文字： $.showLoading('玩命加载中...');
        //自定义宽高： $.showLoading('努力加载中...',140,40);
        $.showLoading();
    });

    //显示前的回调方法
    $('.demo14').hDialog({beforeShow: function(){
        alert('显示前执行');
    }});

    //隐藏后的回调方法
    $('.demo15').hDialog({afterHide: function(){
        alert('隐藏后执行');
    }});

    //fadeOut关闭效果
    $('.demo16').hDialog({effect: 'fadeOut'});

    //bounceOut关闭效果
    $('.demo20').hDialog({effect: 'bounceOut'});

    //bounceOutDown关闭效果
    $('.demo21').hDialog({effect: 'bounceOutDown'});

    //bounceOutLeft关闭效果
    $('.demo22').hDialog({effect: 'bounceOutLeft'});

    //bounceOutRight关闭效果
    $('.demo23').hDialog({effect: 'bounceOutRight'});

    //bounceOutUp关闭效果
    $('.demo24').hDialog({effect: 'bounceOutUp'});

    //fadeOutDown关闭效果
    $('.demo25').hDialog({effect: 'fadeOutDown'});

    //fadeOutLeft关闭效果
    $('.demo26').hDialog({effect: 'fadeOutLeft'});

    //fadeOutRight关闭效果
    $('.demo27').hDialog({effect: 'fadeOutRight'});

    //fadeOutUp关闭效果
    $('.demo28').hDialog({effect: 'fadeOutUp'});

    //flipOutX关闭效果
    $('.demo29').hDialog({effect: 'flipOutX'});

    //flipOutY关闭效果
    $('.demo30').hDialog({effect: 'flipOutY'});

    //lightSpeedOut关闭效果
    $('.demo31').hDialog({effect: 'lightSpeedOut'});

    //rotateOut关闭效果
    $('.demo32').hDialog({effect: 'rotateOut'});

    //rotateOutDownLeft关闭效果
    $('.demo33').hDialog({effect: 'rotateOutDownLeft'});

    //rotateOutDownRight关闭效果
    $('.demo34').hDialog({effect: 'rotateOutDownRight'});

    //rotateOutUpLeft关闭效果
    $('.demo35').hDialog({effect: 'rotateOutUpLeft'});

    //rotateOutUpRight关闭效果
    $('.demo36').hDialog({effect: 'rotateOutUpRight'});

    //slideOutUp关闭效果
    $('.demo37').hDialog({effect: 'slideOutUp'});

    //slideOutDown关闭效果
    $('.demo38').hDialog({effect: 'slideOutDown'});

    //slideOutLeft关闭效果
    $('.demo39').hDialog({effect: 'slideOutLeft'});

    //slideOutRight关闭效果
    $('.demo40').hDialog({effect: 'slideOutRight'});

    //zoomOut关闭效果
    $('.demo41').hDialog({effect: 'zoomOut'});

    //zoomOutDown关闭效果
    $('.demo42').hDialog({effect: 'zoomOutDown'});

    //zoomOutLeft关闭效果
    $('.demo43').hDialog({effect: 'zoomOutLeft'});

    //zoomOutRight关闭效果
    $('.demo44').hDialog({effect: 'zoomOutRight'});

    //zoomOutUp关闭效果
    $('.demo45').hDialog({effect: 'zoomOutUp'});

    //rollOut关闭效果
    $('.demo46').hDialog({effect: 'rollOut'});

    //定时关闭
    $('.demo17').hDialog({hideTime: 2000});

    //不显示关闭按钮
    $('.demo18').hDialog({closeHide: false});

    //不显示遮罩
    $('.demo19').hDialog({isOverlay: false});

    //提示后回调
    $('.demo47').click(function(){
        $.tooltip('hello...',1000,true,function(){
            $.tooltip('执行回调...');
        });
    });

    //confirm
    $('.demo48').click(function(){
        $.dialog('confirm','提示','您确认要删除么？',0,function(){
            $.tooltip('删除成功～',2000,true,function(){
                //$.closeDialog();
                $.closeDialog(function(){ alert('还可以回调了。'); });
            });
        });
    });

    //alert
    $('.demo49').click(function(){
        //$.dialog('alert','提示','正在处理中...'); 或者 $.dialog('alert','提示','正在处理中...',0); //不自动关闭
        $.dialog('alert','提示','正在处理中...',2000,function(){ $.tooltip('执行回调...',2000,true); }); //2s自动关闭
    });

    //iframe
    $('.demo50').hDialog({types:2,iframeSrc:'http://css.doyoe.com/',iframeId:'iframeHBox',width:960,height:600});

    //返回顶部
    $.goTop();

    //提交并验证表单
    $('.submitBtn').click(function() {
        var EmailReg = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/; //邮件正则
        var PhoneReg = /^0{0,1}(13[0-9]|15[0-9]|153|156|18[7-9])[0-9]{8}$/ ; //手机正则
        var $nickname = $('.nickname');
        var $email = $('.email');
        var $phone = $('.phone');
        if($nickname.val() == ''){
            $.tooltip('昵称还没填呢...'); $nickname.focus();
        }else if($phone.val() == ''){
            $.tooltip('手机还没填呢...'); $phone.focus();
        }else if(!PhoneReg.test($phone.val())){
            $.tooltip('手机格式错咯...'); $phone.focus();
        }else if($email.val() == ''){
            $.tooltip('邮箱还没填呢...'); $email.focus();
        }else if(!EmailReg.test($email.val())){
            $.tooltip('邮箱格式错咯...'); $email.focus();
        }else{
            $.tooltip('提交成功，2秒后自动关闭',2000,true,function(){
                $el.hDialog('close',{box:'#HBox'});
            });
        }
    });


});
});
$(window).scroll(function() {
    var p = $(window).scrollTop();
});

