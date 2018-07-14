function imageBtnClickListener(){
    $('#imageNoFilter').on('click',function(e){
        $('#imageFilter').text('Image Filter')
        
    });
    $('#hasImage').on('click',function(e){
        $('#imageFilter').text('Has Image')
    });
    $('#noImage').on('click',function(e){
        $('#imageFilter').text('No Image')
        
    });
}


// on document ready auto code execute
$(function () {
    imageBtnClickListener()
});