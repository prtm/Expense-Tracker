function addExpenseBtnListener() {
    $('#add-expense').on('click', function (e) {
        // var csrftoken = getCookie('csrftoken');
        // var name = $('#id_name').val()
        // var price = $('#id_price').val()
        // var photo = $('#id_photo').val()
        console.log('button clicked');

        $('#add-form').submit()

    });
}





$(function () {
    addExpenseBtnListener()
});