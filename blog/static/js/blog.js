$('#modify-btn').click(function () {
    $.ajax({
        type: 'PUT',
        url: '/' + $('#modify-title').val() + '/modify',
        data: {'title' : $('#modify-title').val(), 'content' : $('#modify-content').val()},
        success: function (result) {
            if (result.status == 'ok'){
                location.replace('/' + $('#modify-title').val());
            }
        },
        error: function (error) {
            alert('error');
            location.replace('/' + $('#modify-title').val());
        }
    });
});

$('#delete-btn').click(function () {
    var result = confirm('Delete?');
    if (result) {
        $.ajax({
            type: 'DELETE',
            url: '/' + $('#post_title').val(),
            data: {'title' : $('#post_title').val()},
            success: function (result) {
                if (result.status == 'ok'){
                    location.replace('/');
                }
                else {
                    alert('fail');
                    location.replace('/' + $('#post_title').val());
                }
            },
            error: function (e) {
                alert(e);
            }
        });
    }
});