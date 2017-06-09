$("#upload_file").click(function()
{
    var _xsrf = $("input[name='_xsrf']").val();
    var formData = new FormData($("#uploadForm")[0]);
    $.ajax({
        url: "/upload0",
        type: "POST",
        data: formData,
        async: true,
        cache: false,
        contentType: false,
        processData: false,
    }).done(function(data){
        $("#home_title").html(data);
        alert("上传成功");
    }).fail(function(data){
        alert("上传失败");
    })
});