function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function addExpense(data) {
    $.ajax({
        url: '/api/v1/expense/',
        type: 'POST',
        data: JSON.stringify(data),
        async: true,
        cache: false,
        contentType: 'application/json',
        beforeSend: function () {
            console.log('Uploading...');
            // $('.upload-progress').show();
        },
        complete: function (response) {
            // $('.upload-progress').hide();
            $(':input', '#add-form')
                .not(':button, :submit, :reset, :hidden')
                .val('')
                .prop('checked', false)
                .prop('selected', false);
            console.log("complete", response.statusText)
            location.reload()
            // $('#addModal').modal('toggle');
        }
    });
}



function addExpenseBtnListener() {
    $('#add-expense').on('click', function (e) {
        var csrftoken = getCookie('csrftoken');
        var name = $('#id_name').val()
        var price = $('#id_price').val()

        var data = {}
        data['name'] = name
        data['price'] = price

        if ($('#id_photo').val()) {
            form = new FormData($('#add-form').get(0))
            form.append('csrfmiddlewaretoken', getCookie('csrftoken'));

            $.ajax({
                url: '/image/uploader/',
                type: 'POST',
                data: form,
                async: true,
                cache: false,
                contentType: false,
                enctype: 'multipart/form-data',
                processData: false,
                success: function (response) {
                    data['photo'] = response['uploaded_file_url']
                    addExpense(data)
                },
                error: function (response) {
                    console.log(response);
                }
            });
        } else {
            addExpense(data)
        }

    });
}

function editExpenseBtnListener() {
    $('.fa-edit').on('click', function (e) {

    });
}

function deleteExpense(data) {
    $.ajax({
        url: '/api/v1/expense/' + data + "/",
        type: 'DELETE',
        async: true,
        cache: false,
        contentType: 'application/json',
        beforeSend: function () {
            console.log('Uploading...');
            // $('.upload-progress').show();
        },
        complete: function (response) {
            // $('.upload-progress').hide();
            console.log("complete", response.statusText)
            location.reload()
        }
    });
}

function deleteExpenseBtnListener() {
    $('#delete-expense').on('click', function (e) {
        var uid = $(this).data('uid')
        deleteExpense(uid)
    });
}


function trashIconListener() {
    $('.fa-trash-alt').on('click', function (e) {
        var name = $(this).closest('div').parent().find('.col-sm-4').text();
        var price = $(this).closest('div').parent().find('.text-center').text();
        $('#delete-name').text("Name: " + name)
        $('#delete-price').text("Price: " + price)
        $('#delete-expense').data('uid', $(this).data('uid'))
    });
}




$(function () {
    addExpenseBtnListener()
    editExpenseBtnListener()
    deleteExpenseBtnListener()
    trashIconListener()
});