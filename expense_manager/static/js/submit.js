// get csrf token
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
// clear add edit form logic
function clearformAddEdit() {
    $(':input', '#add-edit-form')
        .not(':button, :submit, :reset, :hidden')
        .val('')
        .prop('checked', false)
        .prop('selected', false);

    $('#add-edit-expense').data('uid', '')
}

// open add edit modal and change heading and button text
function openAddEditModal(isAdd, uid, name, price) {
    if (isAdd) {
        //add modal open
        $('#addEditModalLabel').text('Add Expense')
        $('#add-edit-expense').text('Add')
    } else {
        // edit modal open
        $('#addEditModalLabel').text('Edit Expense')
        $('#add-edit-expense').text('Update')
        $('#add-edit-expense').data('uid', uid)
        $('#id_name').val(name)
        $('#id_price').val(parseFloat(price.substr(1)))
    }
    $('#addEditModal').modal('show');
}

// add Expense
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
            clearformAddEdit()
            console.log("complete", response.statusText)
            location.reload()
            // $('#addModal').modal('toggle');
        }
    });
}


// add button to open modal
function addEditExpenseBtnListener() {
    $('#add-edit-expense').on('click', function (e) {
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
                    // call add edit expense based on uid found or not
                    var uid = $('#add-edit-expense').data('uid')
                    if (uid == '' | uid == null | uid == undefined) {
                        addExpense(data)
                    } else {
                        editExpense(uid, data)
                    }
                },
                error: function (response) {
                    console.log(response);
                }
            });
        } else {
            // call add edit expense based on uid found or not
            var uid = $('#add-edit-expense').data('uid')
            if (uid == '' | uid == null | uid == undefined) {
                addExpense(data)
            } else {
                editExpense(uid, data)
            }
        }

    });
}

// open add modal 
function addContainerListener() {
    $('#addContainer').on('click', function (e) {
        openAddEditModal(true)
    });
}

// edit expense logic
function editExpense(uid, data) {
    $.ajax({
        url: '/api/v1/expense/' + uid + '/',
        type: 'PATCH',
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

// open edit modal
function editIconListener() {
    $('.fa-edit').on('click', function (e) {
        var uid = $(this).closest('div').parent().find('.fa-trash-alt').data('uid');
        var name = $(this).closest('div').parent().find('.col-sm-4').text();
        var price = $(this).closest('div').parent().find('.text-center').text();
        openAddEditModal(false, uid, name, price)
    });
}


// delete expense logic
function deleteExpense(uid) {
    $.ajax({
        url: '/api/v1/expense/' + uid + "/",
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

// modal delete button click listener
function deleteExpenseBtnListener() {
    $('#delete-expense').on('click', function (e) {
        var uid = $(this).data('uid')
        deleteExpense(uid)
    });
}

// open modal for delete expense from trash icon 
function trashIconListener() {
    $('.fa-trash-alt').on('click', function (e) {
        var name = $(this).closest('div').parent().find('.col-sm-4').text();
        var price = $(this).closest('div').parent().find('.text-center').text();
        $('#delete-name').text("Name: " + name)
        $('#delete-price').text("Price: " + price)
        $('#delete-expense').data('uid', $(this).data('uid'))
    });
}



// add edit modal -> on close -> clear form
function closeAddEditModalBtnListener() {
    $('#close-top-button', '#close-bottom-button').on('click', function (e) {
        clearformAddEdit()
    });

}


// on document ready set listeners
$(function () {
    addContainerListener()
    editIconListener()
    addEditExpenseBtnListener()
    trashIconListener()
    deleteExpenseBtnListener()
    closeAddEditModalBtnListener()
});