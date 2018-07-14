// search button listener
function searchBtnClickListener() {
    $('#searchForm').on('submit', function (e) {
        var data = $('#searchInput').val()
        console.log(data);

        if (data != null && data != '' && data != undefined) {
            if (parseFloat(data)) {
                // search for price
                $('#searchInput').prop('name', 'price')
            } else {
                // search for name
                $('#searchInput').prop('name', 'name')
            }
        } else {
            e.preventDefault()
        }
    });
}


// has image or no image logic click listener
function imageBtnClickListener() {
    $('#imageNoFilter').on('click', function (e) {
        $('#imageFilter').text('Image Filter')
    });
    $('#hasImage').on('click', function (e) {
        $('#imageFilter').text('Has Image')
    });
    $('#noImage').on('click', function (e) {
        $('#imageFilter').text('No Image')
    });
}


// on document ready auto code execute
$(function () {
    imageBtnClickListener()
    searchBtnClickListener()
});