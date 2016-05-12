# tdd-django unit_16

Social Auth
===========
https://github.com/omab/python-social-auth

    pip install python-social-auth


settings.py
-----------

        INSTALLED_APPS = (
           ...
           'social.apps.django_app.default',
           ...
        )

        TEMPLATE_CONTEXT_PROCESSORS = (
           'django.contrib.auth.context_processors.auth',
           'django.core.context_processors.debug',
           'django.core.context_processors.i18n',
           'django.core.context_processors.media',
           'django.core.context_processors.static',
           'django.core.context_processors.tz',
           'django.contrib.messages.context_processors.messages',
           'social.apps.django_app.context_processors.backends',
           'social.apps.django_app.context_processors.login_redirect',
        )

        AUTHENTICATION_BACKENDS = (
           'social.backends.facebook.FacebookOAuth2',
           'social.backends.google.GoogleOAuth2',
           'social.backends.twitter.TwitterOAuth',
           'django.contrib.auth.backends.ModelBackend',
        )


        AUTHENTICATION_BACKENDS = (
            'social.backends.amazon.AmazonOAuth2',
            'social.backends.angel.AngelOAuth2',
            'social.backends.aol.AOLOpenId',
            'social.backends.appsfuel.AppsfuelOAuth2',
            'social.backends.beats.BeatsOAuth2',
            'social.backends.behance.BehanceOAuth2',
            'social.backends.belgiumeid.BelgiumEIDOpenId',
            'social.backends.bitbucket.BitbucketOAuth',
            'social.backends.box.BoxOAuth2',
            'social.backends.clef.ClefOAuth2',
            'social.backends.coinbase.CoinbaseOAuth2',
            'social.backends.coursera.CourseraOAuth2',
            'social.backends.dailymotion.DailymotionOAuth2',
            'social.backends.deezer.DeezerOAuth2',
            'social.backends.disqus.DisqusOAuth2',
            'social.backends.douban.DoubanOAuth2',
            'social.backends.dropbox.DropboxOAuth',
            'social.backends.dropbox.DropboxOAuth2',
            'social.backends.eveonline.EVEOnlineOAuth2',
            'social.backends.evernote.EvernoteSandboxOAuth',
            'social.backends.facebook.FacebookAppOAuth2',
            'social.backends.facebook.FacebookOAuth2',
            'social.backends.fedora.FedoraOpenId',
            'social.backends.fitbit.FitbitOAuth2',
            'social.backends.flickr.FlickrOAuth',
            'social.backends.foursquare.FoursquareOAuth2',
            'social.backends.github.GithubOAuth2',
            'social.backends.google.GoogleOAuth',
            'social.backends.google.GoogleOAuth2',
            'social.backends.google.GoogleOpenId',
            'social.backends.google.GooglePlusAuth',
            'social.backends.google.GoogleOpenIdConnect',
            'social.backends.instagram.InstagramOAuth2',
            'social.backends.jawbone.JawboneOAuth2',
            'social.backends.kakao.KakaoOAuth2',
            'social.backends.linkedin.LinkedinOAuth',
            'social.backends.linkedin.LinkedinOAuth2',
            'social.backends.live.LiveOAuth2',
            'social.backends.livejournal.LiveJournalOpenId',
            'social.backends.mailru.MailruOAuth2',
            'social.backends.mendeley.MendeleyOAuth',
            'social.backends.mendeley.MendeleyOAuth2',
            'social.backends.mineid.MineIDOAuth2',
            'social.backends.mixcloud.MixcloudOAuth2',
            'social.backends.nationbuilder.NationBuilderOAuth2',
            'social.backends.odnoklassniki.OdnoklassnikiOAuth2',
            'social.backends.open_id.OpenIdAuth',
            'social.backends.openstreetmap.OpenStreetMapOAuth',
            'social.backends.persona.PersonaAuth',
            'social.backends.podio.PodioOAuth2',
            'social.backends.rdio.RdioOAuth1',
            'social.backends.rdio.RdioOAuth2',
            'social.backends.readability.ReadabilityOAuth',
            'social.backends.reddit.RedditOAuth2',
            'social.backends.runkeeper.RunKeeperOAuth2',
            'social.backends.skyrock.SkyrockOAuth',
            'social.backends.soundcloud.SoundcloudOAuth2',
            'social.backends.spotify.SpotifyOAuth2',
            'social.backends.stackoverflow.StackoverflowOAuth2',
            'social.backends.steam.SteamOpenId',
            'social.backends.stocktwits.StocktwitsOAuth2',
            'social.backends.stripe.StripeOAuth2',
            'social.backends.suse.OpenSUSEOpenId',
            'social.backends.thisismyjam.ThisIsMyJamOAuth1',
            'social.backends.trello.TrelloOAuth',
            'social.backends.tripit.TripItOAuth',
            'social.backends.tumblr.TumblrOAuth',
            'social.backends.twilio.TwilioAuth',
            'social.backends.twitter.TwitterOAuth',
            'social.backends.vk.VKOAuth2',
            'social.backends.weibo.WeiboOAuth2',
            'social.backends.wunderlist.WunderlistOAuth2',
            'social.backends.xing.XingOAuth',
            'social.backends.yahoo.YahooOAuth',
            'social.backends.yahoo.YahooOpenId',
            'social.backends.yammer.YammerOAuth2',
            'social.backends.yandex.YandexOAuth2',
            'social.backends.vimeo.VimeoOAuth1',
            'social.backends.lastfm.LastFmAuth',
            'social.backends.moves.MovesOAuth2',
            'social.backends.vend.VendOAuth2',
            'social.backends.email.EmailAuth',
            'social.backends.username.UsernameAuth',
            'django.contrib.auth.backends.ModelBackend',
        )

        AUTH_USER_MODEL = 'app.CustomUser'

        LOGIN_URL = '/login/'
        LOGIN_REDIRECT_URL = '/done/'
        URL_PATH = ''
        SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
        SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
        SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/userinfo.profile'
        ]

        # SOCIAL_AUTH_EMAIL_FORM_URL = '/signup-email'
        SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
        SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'example.app.mail.send_validation'
        SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email-sent/'
        # SOCIAL_AUTH_USERNAME_FORM_URL = '/signup-username'
        SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'

        SOCIAL_AUTH_PIPELINE = (
            'social.pipeline.social_auth.social_details',
            'social.pipeline.social_auth.social_uid',
            'social.pipeline.social_auth.auth_allowed',
            'social.pipeline.social_auth.social_user',
            'social.pipeline.user.get_username',
            'example.app.pipeline.require_email',
            'social.pipeline.mail.mail_validation',
            'social.pipeline.user.create_user',
            'social.pipeline.social_auth.associate_user',
            'social.pipeline.debug.debug',
            'social.pipeline.social_auth.load_extra_data',
            'social.pipeline.user.user_details',
            'social.pipeline.debug.debug'
        )

template
---------
        {% load backend_utils %}
        <!doctype html>
        <html>
          <head>
            <title>Python Social Auth</title>
            <link href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
            <link href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css" rel="stylesheet">
            <link href="//netdna.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
            <style>
              h1 { padding: 0 30px; }
              .col-md-2 { width: 18.6667%; }
              .buttons { display: block; table-layout: fixed; border-radius: 7px; border: 1px solid #ccc;
                         margin: 20px; background: #eee; padding: 30px; }
              .buttons > div .btn { margin: 5px 10px; }
              .buttons > div:not(:first-child) { margin-top: 10px; border-top: 1px solid #ccc;
                                                 padding-top: 10px; text-align: center; }
              .user-details { text-align: center; font-size: 16px; font-weight: bold; }
              .disconnect-form { padding: 0; margin: 0px 10px; }
              .disconnect-form > a { display: block; margin: 5px 0 !important; }
            </style>
          </head>
          <body>
            <h1>Python Social Auth</h1>

            <div class="buttons">
              {% if user.is_authenticated %}
                <div class="user-details">
                  You are logged in as <code>{{ user.username }}</code>!
                </div>
              {% endif %}

              <div class="social">
                {% for sublist in available_backends|social_backends %}
                  <div class="row">
                    {% for name, backend in sublist %}
                      {% associated backend %}
                      {% if association %}
                        <form class="disconnect-form col-md-2" id="{{ name }}-disconnect" action="{% url "social:disconnect_individual" backend=association.provider association_id=association.id %}" method="post">{% csrf_token %}
                          <a class="btn btn-danger" name="{{ backend|backend_class }}" href="#">
                            <i class="fa fa-{{ name|icon_name }}"></i>
                            Disconnect {{ backend|backend_name }}
                          </a>
                        </form>
                      {% else %}
                        {% if name == "google-plus" %}
                          <div class="col-md-2 btn btn-default" id="{{ name }}-button" name="{{ backend|backend_class }}">
                            <i class="fa fa-{{ name|icon_name }}"></i>
                            {{ backend|backend_name }}
                          </div>
                        {% else %}
                          <a class="col-md-2 btn btn-default" id="{{ name }}-button" name="{{ backend|backend_class }}" href="{% url "social:begin" backend=name %}">
                            <i class="fa fa-{{ name|icon_name }}"></i>
                            {{ backend|backend_name }}
                          </a>
                        {% endif %}
                      {% endif %}
                    {% endfor %}
                  </div>
                {% endfor %}
              </div>

              <div class="legacy">
                {% for name, backend in available_backends|legacy_backends %}
                  {% associated backend %}
                  {% if association %}
                    <form class="disconnect-form" action="{% url "social:disconnect_individual" backend=association.provider association_id=association.id %}" method="post">{% csrf_token %}
                      <a class="btn btn-danger" name="{{ backend|backend_class }}" href="#">
                        <i class="fa fa-{{ name|icon_name }}"></i>
                        Disconnect {{ backend|backend_name }}
                      </a>
                    </form>
                  {% else %}
                    <a class="btn btn-default" name="{{ backend|backend_class }}" href="{% url "social:begin" backend=name %}">
                      <i class="fa fa-{{ name|icon_name }}"></i>
                      {{ backend|backend_name }}
                    </a>
                  {% endif %}
                {% endfor %}

                <a class="btn btn-info" name="ajax-login" href="#">
                  <i class="fa fa-refresh"></i>
                  Ajax
                </a>
              </div>

              <div>
                <a class="btn btn-primary" href="/logout/" id="logout">
                  <i class="fa fa-sign-out"></i>
                  Logout
                </a>
              </div>
            </div>

            <div id="username-modal" class="modal fade">
              <form action="{% url "social:complete" "username" %}" method="post" role="form">{% csrf_token %}
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                      <h4 class="modal-title">Email Authentication</h4>
                    </div>

                    <div class="modal-body">
                      <div class="form-group">
                        <label class="control-label" for="username">Username:</label>
                        <input class="form-control" id="username" type="text" name="username" value="" />
                      </div>

                      <div class="form-group">
                        <label class="control-label" for="password">Password:</label>
                        <input class="form-control" id="password" type="password" name="password" value="" />
                      </div>

                      <div class="form-group">
                        <label class="control-label" for="fullname">Full name:</label>
                        <input class="form-control" id="fullname" type="text" name="fullname" value="" />
                      </div>
                    </div>

                    <div class="modal-footer">
                      <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                      <button type="button" class="btn btn-primary">Login</button>
                    </div>
                  </div>
                </div>
              </form>
            </div>

            <div id="email-modal" class="modal fade">
              <form action="{% url "social:complete" "email" %}" method="post" role="form">{% csrf_token %}
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                      <h4 class="modal-title">Email Authentication</h4>
                    </div>

                    <div class="modal-body">
                      <div class="form-group">
                        <label class="control-label" for="email">Email address:</label>
                        <input class="form-control" id="email" type="email" name="email" value="" />
                      </div>

                      <div class="form-group">
                        <label class="control-label" for="password">Password:</label>
                        <input class="form-control" id="password" type="password" name="password" value="" />
                      </div>

                      <div class="form-group">
                        <label class="control-label" for="fullname">Full name:</label>
                        <input class="form-control" id="fullname" type="text" name="fullname" value="" />
                      </div>
                    </div>

                    <div class="modal-footer">
                      <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                      <button type="button" class="btn btn-primary">Login</button>
                    </div>
                  </div>
                </div>
              </form>
            </div>

            <div id="livejournal-modal" class="modal fade">
              <form action="{% url "social:begin" "livejournal" %}" method="post" role="form">{% csrf_token %}
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                      <h4 class="modal-title">LiveJournal OpenId Authentication</h4>
                    </div>

                    <div class="modal-body">
                      <div class="form-group">
                        <label class="control-label" for="openid_lj_identifier">LiveJournal ID:</label>
                        <input class="form-control" id="openid_lj_identifier" type="text" value="" name="openid_lj_user" />
                      </div>
                    </div>

                    <div class="modal-footer">
                      <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                      <button type="button" class="btn btn-primary">Login</button>
                    </div>
                  </div>
                </div>
              </form>
            </div>

            <div id="openid-modal" class="modal fade">
              <form action="{% url "social:begin" backend="openid" %}" method="post" role="form">{% csrf_token %}
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                      <h4 class="modal-title">Generic OpenId Authentication</h4>
                    </div>

                    <div class="modal-body">
                      <div class="form-group">
                        <label class="control-label" for="openid_identifier">OpenId Provider:</label>
                        <input class="form-control" id="openid_identifier" type="text" value="" name="openid_identifier" />
                      </div>
                    </div>

                    <div class="modal-footer">
                      <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                      <button type="button" class="btn btn-primary">Login</button>
                    </div>
                  </div>
                </div>
              </form>
            </div>

            <div id="ajax-login-modal" class="modal fade">
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title">Ajax Authentication by AccessToken</h4>
                  </div>

                  <div class="modal-body">
                    <form action="#" method="post" class="form-horizontal" role="form">{% csrf_token %}
                      <div class="form-group">
                        <label class="control-label" for="backend">Backend:</label>
                        <select class="form-control" name="backend">
                          <option value=""></option>
                          {% for name, backend in available_backends|oauth_backends %}
                            <option value="{{ name }}">{{ backend|backend_name }}</option>
                          {% endfor %}
                        </select>
                      </div>

                      <div class="form-group">
                        <label class="control-label" for="access_token">Access token:</label>
                        <input class="form-control" id="access_token" name="access_token" type="text" value="" placeholder="OAuth1 or OAuth2 access token">
                      </div>

                      <div class="form-group">
                        <label class="control-label" for="access_token_secret">Access token secret:</label>
                        <input class="form-control" id="access_token_secret" name="access_token_secret" type="text" value="" placeholder="OAuth1 access token secret">
                      </div>
                    </form>

                    <div class="login-result" style="display: none;">
                      <p><strong>User Id:</strong><span class="user-id"></span></p>
                      <p><strong>Username:</strong><span class="user-username"></span></p>
                      <p>This page will be reloaded in 10s and the user should be logged in.</p>
                    </div>
                  </div>

                  <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary">Login</button>
                  </div>
                </div>
              </div>
            </div>

            <div id="persona-modal" class="modal fade">
              <form action="{% url "social:complete" backend="persona" %}" method="post">{% csrf_token %}
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                      <h4 class="modal-title">Mozilla Persona Authentication</h4>
                    </div>

                    <div class="modal-body">
                      <p>Login with Mozilla Persona by clicking the <code>Login</code> button below.</p>
                      <input type="hidden" name="assertion" value="" />
                    </div>

                    <div class="modal-footer">
                      <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                      <button type="button" class="btn btn-primary">Login</button>
                    </div>
                  </div>
                </div>
              </form>
            </div>

            {% if backend %}
              <div id="email-required-modal" class="modal fade">
                <form action="{% url "social:complete" backend=backend %}" method="post" role="form">{% csrf_token %}
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                        <h4 class="modal-title">Email required</h4>
                      </div>

                      <div class="modal-body">
                        <p>An email address is required.</p>
                        <div class="form-group">
                          <label class="control-label" for="email">Email address:</label>
                          <input class="form-control" id="email" type="email" name="email" value="" />
                        </div>
                      </div>

                      <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary">Continue</button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            {% endif %}

            <div id="validation-sent-modal" class="modal fade">
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title">Email Validation Sent</h4>
                  </div>

                  <div class="modal-body">
                    <p>An email validation was sent{% if email %} to <code>{{ email }}</code>{% endif %}.</p>
                    <p>Click the link sent to finish the authentication process.</p>
                  </div>

                  <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                  </div>
                </div>
              </div>
            </div>

            {% if plus_id %}
            <script src="https://apis.google.com/js/api:client.js"></script>
            <script type="text/javascript">
                gapi.load('auth2', function () {
                  var auth2;

                  auth2 = gapi.auth2.init({
                    client_id: "{{ plus_id }}",
                    scope: "{{ plus_scope }}"
                  });

                  auth2.then(function () {
                    var button = document.getElementById("google-plus-button");
                    console.log("User is signed-in in Google+ platform?", auth2.isSignedIn.get() ? "Yes" : "No");

                    if (button) {
                      auth2.attachClickHandler(button, {}, function (googleUser) {
                        var authResponse = googleUser.getAuthResponse();
                        var $form;
                        var $input;

                        $form = $("<form>");
                        $form.attr("action", "{% url "social:complete" backend="google-plus" %}");
                        $form.attr("method", "post");
                        $input = $("<input>");
                        $input.attr("name", "access_token");
                        $input.attr("value", authResponse.access_token);
                        $form.append($input);
                        $form.append("{% csrf_token %}");
                        $(document.body).append($form);
                        $form.submit();
                      });
                    } else if (auth2.isSignedIn.get()) {
                      $('#logout').on('click', function (event) {
                        event.preventDefault();

                        auth2.signOut().then(function () {
                          console.log("Logged out from Google+ platform");
                          document.location = $(event.target).attr('href');
                        });
                      });
                    }
                  });
                });
            </script>
            {% endif %}

            <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
            <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
            <script src="https://login.persona.org/include.js" type="text/javascript"></script>

            <script type="text/javascript">
              var modalDialog = function (modalId, modalLinkName, submitHandler) {
                var $modal;

                $modal = $(modalId).modal({show: false});

                $modal.on('click', '.btn-primary', submitHandler || function (event) {
                  event.preventDefault();
                  $modal.find('form').submit();
                });

                if (modalLinkName) {
                  $('a[name="' + modalLinkName + '"]').on('click', function (event) {
                    event.preventDefault();
                    $modal.modal('toggle');
                  });
                }

                return $modal;
              };

              $(function () {
                var $validationModal, $emailRequired;

                modalDialog('#livejournal-modal', 'livejournal');
                modalDialog('#openid-modal', 'openid');
                modalDialog('#email-modal', 'email');
                modalDialog('#username-modal', 'username');
                $validationModal = modalDialog('#validation-sent-modal');
                $emailRequired = modalDialog('#email-required-modal');

                modalDialog('#ajax-login-modal', 'ajax-login', function (event) {
                  var $backend, $accessToken, $accessTokenSecret, $fields, $result;
                  event.preventDefault();

                  $modal = $(this).closest('.modal');
                  $form = $modal.find('form');
                  $backend = $modal.find('[name="backend"]');
                  $accessToken = $modal.find('[name="access_token"]');
                  $accessTokenSecret = $modal.find('[name="access_token_secret"]');
                  $result = $modal.find('.login-result');

                  $.get('/ajax-auth/' + $backend.val() + '/', {
                    access_token: $accessToken.val(),
                    access_token_secret: $accessTokenSecret.val(),
                  }, function (data, xhr, response) {
                    $result.find('.user-id').html(data.id);
                    $result.find('.user-username').html(data.username);
                    $form.hide();
                    $result.show();
                    setTimeout(function () { window.location = '/'; }, 10000);
                  }, 'json')
                });

                modalDialog('#persona-modal', 'persona', function (event) {
                  var $form;
                  event.preventDefault();

                  $form = $(this).closest('form');
                  navigator.id.get(function (assertion) {
                    if (assertion) {
                      $form.find('[name="assertion"]').val(assertion)
                      $form.submit();
                    } else {
                      alert('An error occurred while getting your assertion, try again.');
                    }
                  });
                });

                $('.disconnect-form').on('click', 'a.btn', function (event) {
                  event.preventDefault();
                  $(event.target).closest('form').submit();
                });

                {% if validation_sent %}
                  $validationModal.modal('show');
                {% endif %}

                {% if email_required %}
                  $emailRequired.modal('show');
                {% endif %}
              });
            </script>
          </body>
        </html>

templatetags/backend_utils.py
-----------------------------
            import re

            from django import template

            from social.backends.oauth import OAuthAuth


            register = template.Library()

            name_re = re.compile(r'([^O])Auth')


            @register.filter
            def backend_name(backend):
                name = backend.__class__.__name__
                name = name.replace('OAuth', ' OAuth')
                name = name.replace('OpenId', ' OpenId')
                name = name.replace('Sandbox', '')
                name = name_re.sub(r'\1 Auth', name)
                return name


            @register.filter
            def backend_class(backend):
                return backend.name.replace('-', ' ')


            @register.filter
            def icon_name(name):
                return {
                    'stackoverflow': 'stack-overflow',
                    'google-oauth': 'google',
                    'google-oauth2': 'google',
                    'google-openidconnect': 'google',
                    'yahoo-oauth': 'yahoo',
                    'facebook-app': 'facebook',
                    'email': 'envelope',
                    'vimeo': 'vimeo-square',
                    'linkedin-oauth2': 'linkedin',
                    'vk-oauth2': 'vk',
                    'live': 'windows',
                    'username': 'user',
                }.get(name, name)


            @register.filter
            def social_backends(backends):
                backends = [(name, backend) for name, backend in backends.items()
                                if name not in ['username', 'email']]
                backends.sort(key=lambda b: b[0])
                return [backends[n:n + 10] for n in range(0, len(backends), 10)]


            @register.filter
            def legacy_backends(backends):
                backends = [(name, backend) for name, backend in backends.items()
                                if name in ['username', 'email']]
                backends.sort(key=lambda b: b[0])
                return backends


            @register.filter
            def oauth_backends(backends):
                backends = [(name, backend) for name, backend in backends.items()
                                if issubclass(backend, OAuthAuth)]
                backends.sort(key=lambda b: b[0])
                return backends


            @register.simple_tag(takes_context=True)
            def associated(context, backend):
                user = context.get('user')
                context['association'] = None
                if user and user.is_authenticated():
                    try:
                        context['association'] = user.social_auth.filter(
                            provider=backend.name
                        )[0]
                    except IndexError:
                        pass
                return ''

pipeline.py
-----------
        from django.shortcuts import redirect

        from social.pipeline.partial import partial


        @partial
        def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
            if kwargs.get('ajax') or user and user.email:
                return
            elif is_new and not details.get('email'):
                email = strategy.request_data().get('email')
                if email:
                    details['email'] = email
                else:
                    return redirect('require_email')
mail.py
-------
        from django.conf import settings
        from django.core.mail import send_mail
        from django.core.urlresolvers import reverse


        def send_validation(strategy, backend, code):
            url = '{0}?verification_code={1}'.format(
                reverse('social:complete', args=(backend.name,)),
                code.code
            )
            url = strategy.request.build_absolute_uri(url)
            send_mail('Validate your account', 'Validate your account {0}'.format(url),
                      settings.EMAIL_FROM, [code.email], fail_silently=False)

decorators.py
-------------
        from functools import wraps

        from django.template import RequestContext
        from django.shortcuts import render_to_response


        def render_to(tpl):
            def decorator(func):
                @wraps(func)
                def wrapper(request, *args, **kwargs):
                    out = func(request, *args, **kwargs)
                    if isinstance(out, dict):
                        out = render_to_response(tpl, out, RequestContext(request))
                    return out
                return wrapper
            return decorator

views.py
--------

import json

        from django.conf import settings
        from django.http import HttpResponse, HttpResponseBadRequest
        from django.shortcuts import redirect
        from django.contrib.auth.decorators import login_required
        from django.contrib.auth import logout as auth_logout, login

        from social.backends.oauth import BaseOAuth1, BaseOAuth2
        from social.backends.google import GooglePlusAuth
        from social.backends.utils import load_backends
        from social.apps.django_app.utils import psa

        from .decorators import render_to


        def logout(request):
            """Logs out user"""
            auth_logout(request)
            return redirect('/')


        def context(**extra):
            return dict({
                'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
                'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
                'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
            }, **extra)


        @render_to('home.html')
        def home(request):
            """Home view, displays login mechanism"""
            if request.user.is_authenticated():
                return redirect('done')
            return context()


        @login_required
        @render_to('home.html')
        def done(request):
            """Login complete view, displays user data"""
            return context()


        @render_to('home.html')
        def validation_sent(request):
            return context(
                validation_sent=True,
                email=request.session.get('email_validation_address')
            )


        @render_to('home.html')
        def require_email(request):
            backend = request.session['partial_pipeline']['backend']
            return context(email_required=True, backend=backend)


        @psa('social:complete')
        def ajax_auth(request, backend):
            if isinstance(request.backend, BaseOAuth1):
                token = {
                    'oauth_token': request.REQUEST.get('access_token'),
                    'oauth_token_secret': request.REQUEST.get('access_token_secret'),
                }
            elif isinstance(request.backend, BaseOAuth2):
                token = request.REQUEST.get('access_token')
            else:
                raise HttpResponseBadRequest('Wrong backend type')
            user = request.backend.do_auth(token, ajax=True)
            login(request, user)
            data = {'id': user.id, 'username': user.username}
            return HttpResponse(json.dumps(data), mimetype='application/json')

urls.py
-------
        from django.conf.urls import patterns, include, url
        from django.contrib import admin



        urlpatterns = [
            
            url(r'^email-sent/', views.validation_sent),
            url(r'^login/$', views.home),
            url(r'^logout/$', views.logout),
            url(r'^done/$', views.done, name='done'),
            url(r'^ajax-auth/(?P<backend>[^/]+)/$', views.ajax_auth,
                name='ajax-auth'),
            url(r'^email/$', views.require_email, name='require_email'),
            url(r'', include('social.apps.django_app.urls', namespace='social'))
        ]


URLs:
-----

            urlpatterns = [
                
                url(r'^$', views.home, name='main'),
                
                url(r'', include('social.apps.django_app.urls', namespace='social')),
                url(r'^shop/', include('shop.urls', namespace='shop')),
                url(r'^reviews/', include('reviews.urls', namespace='reviews')),
                url(r'^tinymce/', include('tinymce.urls')),
                url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                url(r'^users/', include('userprofiles.urls', namespace="users")),
                
            ]


migrate
-------

        ./manage.py migrate


Регистрации в сетях
-------------------
Для начала нам надо получить ключи от необходимых социальных сетей, на странице проекта в GitHub есть инструкции для множества социальных сетей.

Facebook
--------
Зайдите на https://developers.facebook.com/apps/ и нажмите на + Create New App. Введите название приложения (название сайта или проекта), после сабмита формы вы увидите реквизиты "App ID" и "App Secret".

Добавьте их в свой settings.py, пример:

FACEBOOK_APP_ID = '696381432507483'
FACEBOOK_API_SECRET = '15afb0bbeb173aae12e8e875ffccc7a4'
Теперь заполните поле "App Domains", укажите через пробел домены (например один локальный, другой продакшен домен). Поставьте галочку на "Website with Facebook Login" и введите адрес для редиректа, я редиректю в корень продакшен сайта.

Twitter
-------
Зайдите на https://dev.twitter.com/ и введите логин и пароль от вашей учетной записи в Twitter. Далее заходите на https://dev.twitter.com/apps и жмёте на Create a new application, заполните нужные поля и соглашаетесь с правилами, после чего вы получите "Consumer key" и "Consumer secret".

Добавьте их в settings.py, пример:

TWITTER_CONSUMER_KEY = 'G2wMq4KYpTmgZDcjg0EzQ'
TWITTER_CONSUMER_SECRET = 'rGHMGIbOwIEpoxjXzOahc2KmvxY8h10DpZ90LwqEjec'
По умолчанию вам выдадут Access level "Read-only", для авторизации этого вам хватит. Рекомендую прочитать The Application Permission Model.

Вконтакте
---------
Зайдите на страницу http://vk.com/developers.php и нажмите Создать приложение, выберите Тип "Веб-сайт" и введите адрес сайта и имя домена. В ответ получите "ID приложения" и "Защищенный ключ".

Добавьте их в settings.py, пример:

VK_APP_ID = '1234567'
VKONTAKTE_APP_ID = VK_APP_ID
VK_API_SECRET = 'Q0owlQESOXRYd2lcgnLa'
VKONTAKTE_APP_SECRET = VK_API_SECRET

Google+
-------
Зайдите на страницу https://code.google.com/apis/console/ , нажмите Create, введите требуемые данные и во вкладке API Access увидите "Client ID" и "Client secret".

Добавьте их в settings.py, пример:

GOOGLE_OAUTH2_CLIENT_ID = '123456789.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'p0dJSDjs-dAJsdSAdaSDadasdrt'

GitHub
------
Зайдите на страницу https://github.com/settings/applications/new и введите логин и пароль от вашей учетной записи в GitHub. Введите имя приложения, адреса сайта для "URL" и "Callback URL". И получите "Client ID" и "Client Secret", после чего добавьте их в settings.py:

GITHUB_APP_ID = 'da3bad06987041629b96'


template:
---------
        <ul class="nav  navbar-nav navbar-right">
            {% if user.is_authenticated %}
            <li><a href="{% url 'users:logout' %}">Logout</a></li>
            <li><a href="{% url 'users:profile' slug=user.username %}">{{ user.username }}</a></li>
            {% else %}
            <li><a href="{% url 'users:userprofiles_registration' %}">Register</a></li>
            <li><a href="{% url 'users:login' %}">Login</a></li>
            <li><a href="{% url 'social:begin' 'facebook' %}?next={{ request.path }}">Login with Facebook</a></li>
            <li><a href="{% url 'social:begin' 'google-oauth2' %}?next={{ request.path }}">Login with Google</a></li>
            <li><a href="{% url 'social:begin' 'twitter' %}?next={{ request.path }}">Login with Twitter</a></li>
          {% endif %}
         </ul>


Create an application
---------------------
https://apps.twitter.com/app/new

Application Details
Name * djangosite

Your application name. This is used to attribute the source of a tweet and in user-facing authorization screens. 32 characters max.
Description * Django dev site

Your application description, which will be shown in user-facing authorization screens. Between 10 and 200 characters max.
Website *

http://127.0.0.1:8000

Callback URL    http://127.0.0.1:8000/home

Your application's publicly accessible home page, where users can go to download, make use of, or find out more information about your application. This fully-qualified URL is used in the source attribution for tweets created by your application and will be shown in user-facing authorization screens.
(If you don't have a URL yet, just put a placeholder here but remember to change it later.)
Callback URL

Where should we return after successfully authenticating? OAuth 1.0a applications should explicitly specify their oauth_callback URL on the request token step, regardless of the value given here. To restrict your application from using callbacks, leave this field blank.

Developer Agreement

Yes, I agree

Далее надо читать API конкретной сети. 
--------------------------------------
Вот библиотеки которые могут вам помочь:

Twitter - https://pypi.python.org/pypi/tweepy/ 
Facebook - https://pypi.python.org/pypi/facebook-sdk
Google+ - https://pypi.python.org/pypi/google-api-python-client
Vk - https://pypi.python.org/pypi/vkontakte


API Twitter
===========
https://pypi.python.org/pypi/python-twitter/

twitter 1.17.1
An API and command-line toolset for Twitter (twitter.com)


 pip install twitter

django-classy-tags
------------------
http://django-classy-tags.readthedocs.io/en/latest/

django-classy-tags is an approach at making writing template tags in Django easier, shorter and more fun by providing an extensible argument parser which reduces most of the boiler plate code you usually have to write when coding custom template tags.


    pip install django-classy-tags

django-appconf
--------------
http://django-appconf.readthedocs.io/en/latest/
A helper class for handling configuration defaults of packaged Django apps gracefully.

Это приложение предопределяет собственные классы AppConfig Django, которые действуют как "объекты хранения метаданных для приложения" во время работы механизма загрузки приложения в Django.

   pip install django-appconf



models.py
---------
from __future__ import unicode_literals
from appconf import AppConf

class TwitterConf(AppConf):
    class Meta:
        prefix = 'twitter'
        required = ['OAUTH_TOKEN', 'OAUTH_SECRET', 'CONSUMER_KEY', 'CONSUMER_SECRET']


модуль __future__
------------------

Хорошей практикой является применение deprecated нотаций (помечать, что какой-то метод/функционал будет удален в такой-то версии) Можно пойти дальше и указывать какой функционал станет обязательным в следующих версиях.

Если с deprecated еще все более-менее ясно, то как заставить компилятор понимать функционал из будущих версий?

Для этого в Python есть модуль __future__. Этот небольшой по размеру модуль -> https://hg.python.org/cpython/file/3.5/Lib/future.py

И работает он следующим образом: когда компилятор проходится по файлам с исходным кодом, анализатор выявляет импорты из __future__. Если такой есть, то флаги компиляции дополняются этими импортами, это и позволяет собрать нужный байт-код.

Отсюда и следует понятное требование к импортам из __future__ - они должны быть самыми первыми.

Рассмотрим пример, в 3.5 в модуле __future__ появился флаг generator_stop, который реализует логику PEP 0479. Этот PEP позволяет отлавливать исключение StopIteration внутри генератора. Этот функционал станет доступен только в 3.7, но уже в 3.5 можно его использовать.

from __future__ import generator_stop
# super code
когда компилятор заметит первый импорт, то скомпилирует файл с учетом нового функционала.

По ссылке https://docs.python.org/3.5/library/future.html вы найдете список флагов в модуле __future__. 



settings.py
-----------

        # Your access token: Access token
        TWITTER_OAUTH_TOKEN = 'bI1Vr3AtcZWa5THY8RPyZQYF8SXhkYDJnM21Hh7X9'
        # Your access token: Access token secret
        TWITTER_OAUTH_SECRET = '3S2enJFZGrjv4KRA7FK0TaSK2c9s7iMw8pbqje6eYF'
        # OAuth settings: Consumer key
        TWITTER_CONSUMER_KEY = 'gTVg6h1f0qyUj2Z7M5lKmW'
        # OAuth settings: Consumer secret
        TWITTER_CONSUMER_SECRET = 'EGNPWtsKwIzA4I5HIbpXhcdeFfe1DainSuApL'


templatetags/twitter_tag.py
---------------------------

        from __future__ import unicode_literals
        from datetime import datetime
        from six.moves import http_client
        import logging

        from django import template
        from django.conf import settings
        from django.core.cache import cache
        from django.utils import timezone

        from twitter import Twitter, OAuth, TwitterError
        from classytags.core import Tag, Options
        from classytags.arguments import Argument, MultiKeywordArgument

urllib2
-------

urllib2 это модуль Python для работы с URL-адресом. 
Модуль имеет свои функции и классы, которые помогают в работе с URL - basic и digest аутентификации, перенаправлениях, cookie и многое другое.

Чем urllib отличается от urllib2?

В то время как оба модуля призваны делать примерно одно и то же - работать с URL, они имеют разную функциональность. 

urllib2 в качестве аргумента может принимать Request object, чтобы добавлять заголовки к запросу и другое, в то время как urllib может принимать только стринговый URL. 

urllib имеет метод urlencode, который используется для кодирования строки в вид, удовлетворяющий правилам данных в запросах, а urllib2 не имеет такой функции. Из-за этого urllib и urllib2 часто используются вместе.

В официальной документации:
---------------------------
urllib https://docs.python.org/2/library/urllib.html
urllib2 https://docs.python.org/2/library/urllib2.html

Метод urlopen
-------------
urllib2 предлагает очень простой интерфейс, в виде urlopen функции. 
Эта функция способна извлечь URL-адрес с помощью различных протоколов (HTTP, FTP, ...)
Просто передайте URL адрес функции urlopen(), чтобы получить доступ к удаленным данным.

Кроме того, urllib2 предлагает интерфейс обработки распространенных ситуаций -
таких как basic-аутентификация, cookies, прокси-серверы и так далее. Но обо всем, по порядку.

GET запрос к URL
----------------

Для начала, импортируем urllib2 модуль.
Положим ответ сервера в переменную, например response. (response является file-like объектом.)
Теперь читаем данные из response в строковую переменную html
В дальнейшем, проводим какие-либо действие с переменной html.

если существует пробел в адресе, необходимо проенкодить его, используя метод urlencode.

Пример 1
--------
import urllib2

        response = urllib2.urlopen('http://python.org/')
        print response.info()
        html = response.read()
        # делаем что-нибудь
        response.close()

        # также можно использовать URL начинающиеся с "ftp:", "file:", и т.д.

Пример 2
--------
        import urllib2

        response = urllib2.urlopen('http://python.org/')
        print "Ответ (file-like object):", response

        # URL из запроса
        print "The URL is: ", response.geturl()

        # Ответ сервера
        print "This gets the code: ", response.code

        # Заголовки ответа в виде словаря
        print "The Headers are: ", response.info()

        # Достаем дату сервера из заголовков ответа
        print "The Date is: ", response.info()['date']

        # Получаем заголовок 'server' из заголовков 
        print "The Server is: ", response.info()['server']

        # Получаем весь html страницы
        html = response.read()
        print "Get all data: ", html

        # Узнаем длину страницу
        print "Get the length :", len(html)

        for line in response:
         print line.rstrip()


Скачивание файла с помощью urllib2
-----------------------------------
        import urllib2

        # файл для записи
        file = "downloaded_file.html"

        url = "http://www.pythonforbeginners.com/"
        response = urllib2.urlopen(url)

        # откроем файл на запись
        fh = open(file, "w")

        # читаем URL и записываем в локальный файл
        fh.write(response.read())
        fh.close()

        # аналогичный вариант
        with open(file, 'w') as f: f.write(response.read())

пример с скачиванием бинарного файла:
-------------------------------------
        import urllib2

        mp3file = urllib2.urlopen("http://www.example.com/songs/mp3.mp3")

        output = open('test.mp3','wb')
        output.write(mp3file.read())
        output.close()

urllib2 Request
---------------
Если нужно отправить что-то замысловатое, например добавить дополнительные заголовки к запросу, то нужно использовать urllib2.Request.

Вы можете задать исходящие данные в Request, которые хотите отправить на сервере.
Кроме того, вы можете передавать на сервер дополнительную информацию (метаданные) о данных, отправляемых на сервер или о самом запросе, эта информация передается в виде HTTP заголовков.

Если вы хотите отправить POST запрос, нужно сначала создать словарь содержащий необходимые переменные и их значения.


        # Данные, которые хотим отправить
        query_args = { 'q':'query string', 'foo':'bar' }

        # Производим urlencodes для ранее созданного словаря (вот для чего мы импортировали библиотеку urllib вверху)
        data = urllib.urlencode(query_args)

        # Отправляем HTTP POST запрос
        request = urllib2.Request(url, data)

        response = urllib2.urlopen(request)
         
        html = response.read()

        # Выводим результат
        print html


User Agent
----------
Чтобы идентифицировать клиента, который отправляет запрос, будь то браузер или какая-либо программа, умные люди придумали заголовок User-Agent. Который хранит в себе название и версию клиента.
По умолчанию urllib2 идентифицирует себя как Python-urllib/x.y
где x и y - это номера версий Python-релиза.

С urllib2 можно добавить собственные заголовки к запросу.
Причина, по которой нужно изменять User Agent бывают разные, но в большинстве случаев это делается для того, чтобы как можно больше, походить на реального человека, а не скрипт.

При создании Request объекта нужно добавить заголовки в словарь,
для этого используйте опцию add_header().

        import urllib2

        # наш URL
        url = 'http://www.google.com/#q=my_search'

        # Добавляем заголовок. 
        headers = {'User-Agent' : 'Mozilla 5.10'}
        # создаем Request объект. 
        request = urllib2.Request(url, None, headers)

        # или так
        # request.add_header('User-Agent' : 'Mozilla 5.10')

        # Посылаем запрос и получаем ответ
        response = urllib2.urlopen(request)

        # Выводим заголовки
        print response.headers

urllib.urlparse
---------------
urlparse модуль содержит функции для анализа URL строки.

Он определяет стандартный интерфейс разделения Uniform Resource Locator (URL)
строки в несколько дополнительных частей, называемых компонентами (scheme, location, path, query и fragment).

        Скажем, у вас есть URL:
        http://www.python.org:80/index.html
         в нем, будут следующие компоненты:

        schema: http
        location: www.python.org:80
        path: index.html
        query и fragment будут пустыми.

        import urlparse

        url = "http://python.org"
        domain = urlparse.urlsplit(url)[1].split(':')[0]

        print "The domain name of the url is: ", domain


urllib.urlencode
----------------
Когда вы передаете информацию через URL, вы должны убедиться, что в ней используется только определенные, разрешенные символы. 

Разрешенные символы - это любые алфавитные символы, цифры и некоторые специальные
символы, которые имеют значение в строке URL-адреса.

Наиболее часто кодируются символ "пробел". Вы видите этот символ каждый раз, когда вы видите знак "плюс " (+) в URL. Это означает пробел. 
Знак "плюс" выступает как специальный символ, представляющий пробелы в URL

Аргументы могут быть переданы на сервер при их кодировании и последующему добавлению к URL-адресу.


        import urllib

        query_args = { "q":"query string", "sql":"' or 1='1" }
        encoded_args = urllib.urlencode(query_args)

        print 'Encoded:', encoded_args


В результате получим следующее:
        Encoded: q=query+string&sql=%27+or+1%3D%271
пробел преобразовался в символ +, одинарная кавычка в %27.

Python urlencode принимает пару переменная/значение и создает уже кодированную строку.

        from urllib import urlencode

        artist = "Kruder & Dorfmeister"
        artist = urlencode({'ArtistSearch':artist})

        Результатом будет:
        ArtistSearch=Kruder+%26+Dorfmeister

Обработка ошибок
---------------- 

urlopen поднимает URLError, когда он не может обработать ответ сервера. HTTPError является подклассом URLError, и поднимается в конкретном случае - при обработке ошибки, связанной с HTTP.

URLError
--------
Часто, URLError вызывается, потому что нет сетевого соединения или указанный сервер не существует.
В этом случае нам нужен атрибут 'reason', который содержит код и текст сообщения об ошибке. 

        import  urllib2

        request = urllib2.Request('http://www.pretend_server.org')
        try: 
            urllib2.urlopen(request)
        except urllib2.URLError, e:
            print e.reason


HTTPError
---------
Каждый HTTP-ответ от сервера содержит код состояния. Иногда этот код указывает, что сервер не в состоянии обработать запрос.

Обработчик по умолчанию будет обрабатывать некоторые из этих кодов для вас (например,
если ответ "перенаправление", urllib2 обработает это). 
При тех случаях, которые библиотека не может обработать ошибку, urlopen вызывает HTTPError.

        from urllib2 import Request, urlopen, URLError

        req = Request('http://python.org/error.html')

        try:
            response = urlopen(req)

        except URLError, e:

            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason

            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            print 'no error'




        from ..utils import *

        try:
            from urllib2 import URLError
        except ImportError:
            from urllib.error import URLError

urllib.parse.quote
------------------
        urllib.parse.quote(<строка>[, safe='/'][, encoding=None][, errors=None])
заменяет все специальные симолы последовательностями %nn. Цифры, анг­лийские буквы и символы подчеркивания, точки и дефиса не кодируются. Пробелы преобразуются в последовательность %20.

Параметры:  safe (str) – символы, которые преобразовывать нельзя
        >>> quote("Cтpoкa", encoding="cp1251")
        '%D1%F2%F0%EE%EA%E0'
        >>> quote("Cтpoкa", encoding="utf-8")
        '%D0%A1%D1%82%D1%80%D0%BE%D0%BA%D0%B0'

utils.py
--------
        from __future__ import unicode_literals
        import re
        try:
            from urllib import quote
        except ImportError:
            from urllib.parse import quote


        def get_user_cache_key(**kwargs):
            """ Generate suitable key to cache twitter tag context
            """
            key = 'get_tweets_%s' % ('_'.join([str(kwargs[key]) for key in sorted(kwargs) if kwargs[key]]))
            not_allowed = re.compile('[^%s]' % ''.join([chr(i) for i in range(33, 128)]))
            key = not_allowed.sub('', key)
            return key


        def get_search_cache_key(prefix, *args):
            """ Generate suitable key to cache twitter tag context
            """
            key = '%s_%s' % (prefix, '_'.join([str(arg) for arg in args if arg]))
            not_allowed = re.compile('[^%s]' % ''.join([chr(i) for i in range(33, 128)]))
            key = not_allowed.sub('', key)
            return key


        TWITTER_HASHTAG_URL = '<a href="https://twitter.com/search?q=%%23%s">#%s</a>'
        TWITTER_USERNAME_URL = '<a href="https://twitter.com/%s">@%s</a>'


urlize
-------
Конвертирует URL-ы в тексте в “кликабельные” ссылки.

Этот тег конвертирует ссылки с префиксами http://, https://, или www.. Например, http://goo.gl/aia1t будет конвертирован, goo.gl/aia1t – нет.

Так же поддерживаются ссылки состоящие только из домена и заканчивающиеся на один из первоначальных доменов первого уровня (.com, .edu, .gov, .int, .mil, .net, and .org). Например, djangoproject.com будет преобразован.

Ссылки могут быть с завершающей пунктуацией (точка, запятая, закрывающая скобка) и предшествующей пунктуацией (открывающая скобка), urlize все корректно преобразует.

Ссылки созданные urlize содержат атрибут rel="nofollow".

Например:

    {{ value|urlize }}
Если value равно "Check out www.djangoproject.com", будет выведено 

    "Check out <a href="http://www.djangoproject.com" rel="nofollow">www.djangoproject.com</a>".

Фильтр urlize принимает не обязательный аргумент autoescape. Если autoescape равен True, текст ссылки и URL будут экранированы с помощью фильтра escape. Значение по-умолчанию для autoescape равно True.

Если применить urlize к тексту, который содержит HTML, результат будет неверным. Применяйте фильтр только к обычному тексту.


        def urlize_tweet(tweet):
            """ Turn #hashtag and @username in a text to Twitter hyperlinks,
                similar to the ``urlize()`` function in Django.
            """
            text = tweet.get('html', tweet['text'])
            for hash in tweet['entities']['hashtags']:
                text = text.replace('#%s' % hash['text'], TWITTER_HASHTAG_URL % (quote(hash['text'].encode("utf-8")), hash['text']))
            for mention in tweet['entities']['user_mentions']:
                text = text.replace('@%s' % mention['screen_name'], TWITTER_USERNAME_URL % (quote(mention['screen_name']), mention['screen_name']))
            tweet['html'] = text
            return tweet


        def expand_tweet_urls(tweet):
            """ Replace shortened URLs with long URLs in the twitter status, and add the "RT" flag.
                Should be used before urlize_tweet
            """
            if 'retweeted_status' in tweet:
                text = 'RT @{user}: {text}'.format(user=tweet['retweeted_status']['user']['screen_name'],
                                                   text=tweet['retweeted_status']['text'])
                urls = tweet['retweeted_status']['entities']['urls']
            else:
                text = tweet['text']
                urls = tweet['entities']['urls']

            for url in urls:
                text = text.replace(url['url'], '<a href="%s">%s</a>' % (url['expanded_url'], url['display_url']))
            tweet['html'] = text
            return tweet




    register = template.Library()


        class BaseTwitterTag(Tag):
            """ Abstract twitter tag"""

            def get_cache_key(self, args_disct):
                raise NotImplementedError

            def get_json(self, twitter):
                raise NotImplementedError

            def get_api_call_params(self, **kwargs):
                raise NotImplementedError

            def enrich(self, tweet):
                """ Apply the local presentation logic to the fetched data."""
                tweet = urlize_tweet(expand_tweet_urls(tweet))
                # parses created_at "Wed Apr 27 16:08:45 +0000 2008"

                if settings.USE_TZ:
                    tweet['datetime'] = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=timezone.utc)
                else:
                    tweet['datetime'] = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

                return tweet

            def render_tag(self, context, **kwargs):
                cache_key = self.get_cache_key(kwargs)

                try:
                    twitter = Twitter(auth=OAuth(settings.TWITTER_OAUTH_TOKEN,
                                                 settings.TWITTER_OAUTH_SECRET,
                                                 settings.TWITTER_CONSUMER_KEY,
                                                 settings.TWITTER_CONSUMER_SECRET))
                    json = self.get_json(twitter, **self.get_api_call_params(**kwargs))
                except (TwitterError, URLError, ValueError, http_client.HTTPException) as e:
                    logging.getLogger(__name__).error(str(e))
                    context[kwargs['asvar']] = cache.get(cache_key, [])
                    return ''

                json = [self.enrich(tweet) for tweet in json]

                if kwargs['limit']:
                    json = json[:kwargs['limit']]
                context[kwargs['asvar']] = json
                cache.set(cache_key, json)

                return ''



        class UserTag(BaseTwitterTag):
            """ A django template tag to display user's recent tweets.

                :type context: list
                :type username: string
                :type asvar: string
                :type exclude: string
                :type limit: string

                NB: count argument of twitter API is not useful, so we slice it ourselves
                    "We include retweets in the count, even if include_rts is not supplied.
                     It is recommended you always send include_rts=1 when using this API method."

                Examples:
                {% get_tweets for "janusnic" as tweets exclude "replies" limit 10 %}
                {% get_tweets for "janusnic" as tweets exclude "retweets" %}
                {% get_tweets for "janusnic" as tweets exclude "retweets,replies" limit 1 %}
            """
            name = 'get_tweets'
            options = Options(
                'for', Argument('username'),
                'as', Argument('asvar', resolve=False),
                'exclude', Argument('exclude', required=False),
                'limit', Argument('limit', required=False),
            )

            def get_cache_key(self, kwargs_dict):
                return get_user_cache_key(**kwargs_dict)

            def get_api_call_params(self, **kwargs):
                params = {'screen_name': kwargs['username']}
                if kwargs['exclude']:
                    if 'replies' in kwargs['exclude']:
                        params['exclude_replies'] = True
                    if 'retweets' in kwargs['exclude'] or 'rts' in kwargs['exclude']:
                        params['include_rts'] = False
                return params

            def get_json(self, twitter, **kwargs):
                return twitter.statuses.user_timeline(**kwargs)


        class SearchTag(BaseTwitterTag):
            name = 'search_tweets'
            options = Options(
                'for', Argument('q'),
                'as', Argument('asvar', resolve=False),
                MultiKeywordArgument('options', required=False),
                'limit', Argument('limit', required=False),
            )

            def get_cache_key(self, kwargs_dict):
                return get_search_cache_key(kwargs_dict)

            def get_api_call_params(self, **kwargs):
                params = {'q': kwargs['q'].encode('utf-8')}
                params.update(kwargs['options'])
                return params

            def get_json(self, twitter, **kwargs):
                return twitter.search.tweets(**kwargs)['statuses']


        register.tag(UserTag)
        register.tag(SearchTag)

index.html
----------
        {% load twitter_tag %}


        <div class="col-md-4">
          <h2>Latest Tweets from @janusnic</h2>
              {% get_tweets for "janusnic" as tweets %}

              <ul>
              {% for tweet in tweets %}
                  <li>{{ tweet.html|safe }}</li>
              {% endfor %}
              </ul>
          
        </div>
      </div>

Tweet Button
------------
https://about.twitter.com/resources/buttons#tweet

    <a href="https://twitter.com/share" class="twitter-share-button" data-via="janusnic">Tweet</a>
    <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script>


Create an Embedded Timeline 
---------------------------
https://twitter.com/settings/widgets/new


        <a class="twitter-timeline" href="https://twitter.com/janusnic" data-widget-id="730735893250772992">Tweets by @janusnic</a>
        <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>

