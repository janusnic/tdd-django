var ajax = {
    post: function (url, data, callback) {
        $.ajax({
            type: 'POST', url: url, data: data,
            success: function (data) { callback(data); },
            error: function (data) { ajax.error(data); }
        });
    },
    get: function (url, callback) {
        $.ajax({
            type: 'GET', url: url,
            success: function (data) { callback(data); },
            error: function (data) { ajax.error(data); }
        });
    },
    error: function (data) {
        console.log(data);
        alert("There was an error processing your request.\nPlease try again later.");
    },
};
var navigation = {
    goto: function (dir) {
        selector = $("[data-navigate=" + dir + "]:last");
        if (selector.attr("href")) {
            window.location = selector.attr("href");
        }
    },
    init: function () {
        $(document).keydown(function (event) {
            if (event.which == 37) { navigation.goto("left"); }
            if (event.which == 39) { navigation.goto("right"); }
            if (event.which == 40) { navigation.goto("down"); }
            // Only navigate up if we are at the top of the page.
            if (event.which == 38 && $(document).scrollTop() == 0) { navigation.goto("up"); }
        });
    }
};
var form = {
    process: function (data) {
        if (data.url) {
            window.location = data.url;
            return;
        }
        if (data.html) {
            form.showModal(data);
            return;
        }
        ajax.error(data);
    },
    showModal: function (data) {
        $('#modal-window').show();
        $('#modal').html(data.html);
        $("#modal select").chosen();

        $("#modal .cancel").click(function (event) {
            form.hideModal();
        });

        $("#modal form").submit(function (event) {
            event.preventDefault();
            ajax.post($(this).attr("action"), $(this).serialize(), form.process);
        });
    },
    hideModal: function () {
        $('#modal-window').hide();
        $("#modal").html("");
    },
    init: function () {
        $("[data-modal='form']").click(function (event) {
            event.preventDefault();
            ajax.get($(this).attr("href"), form.showModal);
        });
    },
};

var rotate = {
    process: function (data) {
        // Simply reload the image (which will be rotated).
        // Strip off the previous querystring from the image first.
        // Could not find an easy reliable way to rotate in CSS or JS so this will have to do for now.
        img = $('.photo img');
        img.attr("src", img.attr("src").split("?")[0] + "?" + new Date().getTime());
    },
    init: function () {
        $("[data-modal='rotate']").click(function (event) {
            event.preventDefault();
            ajax.post($(this).attr("href"), {}, rotate.process);
        });
    }
};

$(function () {
    navigation.init();
    form.init();
    rotate.init()
});
