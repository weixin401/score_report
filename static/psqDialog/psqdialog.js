function PSQDialog(class_id)
{
    //box-dialog
    var This = this;
    This.box_id = $('#' + class_id);

    This.init = function(mWidth,mHeight)
    {
        This.box_id.css('width',mWidth+"px");
        This.box_id.css('height',mHeight+"px");

        $('.box-dialog_close').html("&#215;");
        $('body').append('<div class="box-background""></div>');
    };

    This.showDialog = function()
    {
        This.box_id.addClass('box-dialog-show');
        $('.box-background').css('display','block');
    };
    This.hideDialog = function()
    {
        This.box_id.removeClass('box-dialog-show');
        $('.box-background').css('display','none');
    };

    $('body').on('click','.box-background',function(){
        This.hideDialog();
    });

    $('.box-dialog_close').click(function(){
        This.hideDialog();
    });
    return This;
}


