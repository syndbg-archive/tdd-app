$(document).ready(function () {
    var loginLink = document.getElementById('login');

    if (loginLink) {
        loginLink.onclick = function () {
            navigator.id.request();
        };
    }

    var currentUser = '{{ user.email }}' || null;
    var csrfToken = '{{ csrf_token }}';
    console.log(currentUser);

    navigator.id.watch({
        loggedInUser: currentUser,
        onlogin: function (assertion) {
            $.post('/accounts/login', {assertion: assertion, csrfmiddlewaretoken: csrfToken})
            .done(function () {
                window.location.reload();
            })
            .fail(function () {
              navigator.id.logout();
            });
        },
        onlogout: function () {
            $.post('/accounts/logout')
            .always(function () {
                window.location.reload();
            });
        }
    });
});
