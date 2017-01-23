$('#modify-btn').click(function () {
    $.ajax({
        type: 'PUT',
        url: '/post/' + $('#modify-title').val() + '/modify',
        data: {'title' : $('#modify-title').val(), 'content' : $('#modify-content').val(), 'tag' : $('#modify-tag').val()},
        success: function (result) {
            if (result.status == 'ok'){
                location.replace('/post/' + $('#modify-title').val());
            }
        },
        error: function (error) {
            alert('error');
            location.replace('/post/' + $('#modify-title').val());
        }
    });
});

$('#delete-btn').click(function () {
    var result = confirm('Delete?');
    if (result) {
        $.ajax({
            type: 'DELETE',
            url: '/post/' + $('#post_title').val(),
            data: {'title' : $('#post_title').val()},
            success: function (result) {
                if (result.status == 'ok'){
                    location.replace('/');
                }
                else {
                    alert('fail');
                    location.replace('/post/' + $('#post_title').val());
                }
            },
            error: function (e) {
                alert(e);
            }
        });
    }
});