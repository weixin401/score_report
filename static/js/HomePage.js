var excel_json;
$("#button_1").on("mouseenter",function()
{
    $("#button_1").css("cursor","pointer");
});
$("#button_1").on("mouseleave",function()
{
    $("#button_1").css("cursor","default");
});
$("#button_2").on("mouseenter",function()
{
    $("#button_2").css("cursor","pointer");
});
$("#button_2").on("mouseleave",function()
{
    $("#button_2").css("cursor","default");
});
$("#button_1").click(function()
{
    //showDialog('upload_dialog');

});
$("#upload_img_box img").click(function(){
    $("#file").val("");
    $("#file").click();
});

$("#file").change(function()
{
    var _xsrf = $("input[name='_xsrf']").val();
    $("#home_title").append(_xsrf);
    var formData = new FormData($("#uploadForm")[0]);
    $.ajax({
        url: "/upload0",
        type: "POST",
        data: formData,
        async: true,
        cache: false,
        contentType: false,
        processData: false
    }).done(function(data){
        $("#home_title").append(data);
        //excel_json = data;
        var jsonObj = eval('(' + data + ')');
        excel_json = data;
        $("#excel_table").html("");
        var html = "<thead><tr>";
        for(var i=0;i<jsonObj.length;i++)
        {
            for(var key in jsonObj[i])
            {
                html+="<th><div class='excel_table_th'> "+key+"<divh></th>"
            }
            break;
        }
        html += "</tr></thead>";
        html += "<tbody>";
        for(var i=0;i<jsonObj.length;i++)
        {
            html += "<tr>";
            for(var key in jsonObj[i])
            {
                html+="<td><div class='excel_table_td'>"+jsonObj[i][key]+"</div></td>"
            }
            html += "</tr>";
        }
        html += "</tbody>";
        $("#excel_table").append(html);
        hideDialog('upload_dialog');
        showDialog('excel_dialog');
    }).fail(function(data){
        alert("上传失败");
    });

});
$("#upload_file").click(function()
{


});
$("#upload_ok_file").click(function(){

    var _xsrf = getCookie("_xsrf");
    var data = {
        "students_score":excel_json,
        "total_score":parseInt("100"),
        "_xsrf":_xsrf
    };
    $.post("/score_report_v0",
        data,
        function(data,status){
            hideDialog("excel_dialog");
            alert(status);
        },
        "json"
    );
});
function showDialog(dialogID)
{
    $('#'+dialogID).fadeIn(150);
    $('#'+dialogID).children('.m-modal-dialog').animate({
        "margin-top": "200px"
    }, 200);
}
function hideDialog(dialogID)
{
    var $modal = $('#'+dialogID);
    $modal.children('.m-modal-dialog').animate({
        "margin-top": "-100%"
    }, 500);
    $modal.fadeOut(100);
}
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}