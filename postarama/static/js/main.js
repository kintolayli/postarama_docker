function rating_up()
{
    var like = $(this);
    var username = like.data('username');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();

    var type = like.data('type');
    var comment_pk = like.data('comment-id');

    var ajax_url;

    if (type === 'comment') {
        ajax_url = "/" + username + "/" + pk + "/" + type + "/" + comment_pk + "/" + action + "/"
    }
    else {
        ajax_url = "/" + username +"/" + pk + "/" + action + "/"
    }

    $.ajax({
        url : ajax_url,
        type: 'POST',
        data: {'obj': pk},

        success: function (response) {
            if (response.user_is_fan) {
                if (response.sum_rating > 0) {
                    dislike.find("[data-count='dislike']").text('+' + response.sum_rating);
                }
                else {
                    dislike.find("[data-count='dislike']").text(response.sum_rating);

                }
                like.children(".btn").attr('disabled', true)


            }
            else {
                if (response.sum_rating > 0) {
                    dislike.find("[data-count='dislike']").text('+' + response.sum_rating);
                }
                else {
                    dislike.find("[data-count='dislike']").text(response.sum_rating);
                }
                dislike.next().children(".btn").removeAttr('disabled', true)
            }
        }
    })
    return false;
}

function rating_down()
{
    var dislike = $(this);
    var username = dislike.data('username');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    var type = dislike.data('type');
    var comment_pk = dislike.data('comment-id');

    var ajax_url;

    if (type === 'comment') {
        ajax_url = "/" + username + "/" + pk + "/" + type + "/" + comment_pk + "/" + action + "/"
    }
    else {
        ajax_url = "/" + username +"/" + pk + "/" + action + "/"
    }

    $.ajax({
        url : ajax_url,
        type: 'POST',
        data : { 'obj' : pk },

        success: function (response) {
            if (response.user_is_hater) {
                if (response.sum_rating > 0) {
                    like.find("[data-count='dislike']").text('+' + response.sum_rating);
                }
                else {
                    like.find("[data-count='dislike']").text(response.sum_rating);
                }
                dislike.children(".btn").attr('disabled', true)

            }
            else {
                if (response.sum_rating > 0) {
                    like.find("[data-count='dislike']").text('+' + response.sum_rating);
                }
                else {
                    like.find("[data-count='dislike']").text(response.sum_rating);
                }
                like.prev().children(".btn").removeAttr('disabled', true)
            }
        }
    });
    return false;
}

function to_bookmarks()
{
    let bookmark = "<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-bookmark\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
        "  <path fill-rule=\"evenodd\" d=\"M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.777.416L8 13.101l-5.223 2.815A.5.5 0 0 1 2 15.5V2zm2-1a1 1 0 0 0-1 1v12.566l4.723-2.482a.5.5 0 0 1 .554 0L13 14.566V2a1 1 0 0 0-1-1H4z\"/>\n" +
        "</svg>";
    let bookmark_fill = "<svg width=\"1em\" height=\"1em\" viewBox=\"0 0 16 16\" class=\"bi bi-bookmark-fill\" fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">\n" +
        "  <path fill-rule=\"evenodd\" d=\"M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.74.439L8 13.069l-5.26 2.87A.5.5 0 0 1 2 15.5V2z\"/>\n" +
        "</svg>";

    var current = $(this);
    var username = current.data('username');
    var pk = current.data('id');
    var action = current.data('action');
    var response_count;

    $.ajax({
        url : "/" + username +"/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (response) {
            if (response.count === 0) {
                response_count = ''
            }
            else {
                response_count = response.count
            }
            if (response.bookmark) {
                current.html(bookmark + ' ' + response_count);
            }
            else {
                current.html(bookmark_fill + ' ' + response_count);
            }
        }
    });

    return false;
}


$(function() {
    $('[data-action="like"]').click(rating_up);
    $('[data-action="dislike"]').click(rating_down);

    $('[data-action="bookmark"]').click(to_bookmarks);
});



