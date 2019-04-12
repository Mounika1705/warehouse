$(function(){
    $('#register').addClass('active');
    var parent = $('#id_employee_id').parent()[0];
    parent.style = 'display:none';
    $('#id_staff').change(function() {
        if(parent.style.display == 'none'){
            parent.removeAttribute('style');
        } else {
            parent.style = 'display:none';
        }
    });
});