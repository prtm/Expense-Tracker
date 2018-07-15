// search button listener
function searchBtnClickListener() {
    $('#searchForm').on('submit', function (e) {
        var data = $('#searchInput').val()
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

function insertParam(key, value) {
    key = encodeURI(key);
    value = encodeURI(value);

    var kvp = document.location.search.substr(1).split('&');
    console.log(kvp);

    var i = kvp.length;
    var x;
    while (i--) {
        x = kvp[i].split('=');

        if (x[0] == 'photo__ne' || x[0] == 'photo' || x[0] == '') {
            kvp.splice(i, 1)
        }
    }

    // not found in current url then add key value
    if (key != '') {
        kvp[kvp.length] = [key, value].join('=')
    }

    //this will reload the page, it's likely better to store this until finished
    document.location.search = kvp.join('&');
}


// has image or no image logic click listener
function imageBtnClickListener() {
    $('#imageNoFilter').on('click', function (e) {
        $('#imageFilter').text('Image Filter')
        insertParam('', '')

    });
    $('#hasImage').on('click', function (e) {
        $('#imageFilter').text('Has Image')
        insertParam('photo__ne', '')
    });
    $('#noImage').on('click', function (e) {
        $('#imageFilter').text('No Image')
        insertParam('photo', '')
    });
}


// on document ready auto code execute
$(function () {
    imageBtnClickListener()
    searchBtnClickListener()
});