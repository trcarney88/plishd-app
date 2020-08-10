'use strict';

$(function() {


  /*
  |--------------------------------------------------------------------------
  | Configure your website
  |--------------------------------------------------------------------------
  |
  | We provided several configuration variables for your ease of development.
  | Read their complete description and modify them based on your need.
  |
  */

  page.config({

    /*
    |--------------------------------------------------------------------------
    | Google API Key
    |--------------------------------------------------------------------------
    |
    | Here you may specify your Google API key if you need to use Google Maps
    | in your application
    |
    | https://developers.google.com/maps/documentation/javascript/get-api-key
    |
    */

    googleApiKey: 'AIzaSyDRBLFOTTh2NFM93HpUA4ZrA99yKnCAsto',

    /*
    |--------------------------------------------------------------------------
    | Google Analytics Tracking
    |--------------------------------------------------------------------------
    |
    | If you want to use Google Analytics, you can specify your Tracking ID in
    | this option. Your key would be a value like: UA-12345678-9
    |
    */

    googleAnalyticsId: 'UA-157437961-1',

    /*
    |--------------------------------------------------------------------------
    | Google reCAPTCHA
    |--------------------------------------------------------------------------
    |
    | reCAPTCHA protects you against spam and other types of automated abuse.
    | Please signup for an API key pair and insert your `Site key` value to the
    | following variable.
    |
    | http://www.google.com/recaptcha/admin
    |
    */

    reCaptchaSiteKey:  '6Ldaf0MUAAAAAHdsMv_7dND7BSTvdrE6VcQKpM-n',

    // See available languages: https://developers.google.com/recaptcha/docs/language
    reCaptchaLanguage: '',

    /*
    |--------------------------------------------------------------------------
    | Disable AOS on mobile
    |--------------------------------------------------------------------------
    |
    | If true, the Animate On Scroll animations don't run on mobile devices.
    |
    */

    disableAOSonMobile: true,

    /*
    |--------------------------------------------------------------------------
    | Smooth Scroll
    |--------------------------------------------------------------------------
    |
    | If true, the browser's scrollbar moves smoothly on scroll and gives your
    | visitor a better experience for scrolling.
    |
    */

    smoothScroll: true,

  });





  /*
  |--------------------------------------------------------------------------
  | Custom Javascript code
  |--------------------------------------------------------------------------
  |
  | Now that you configured your website, you can write additional Javascript
  | code below this comment. You might want to add more plugins and initialize
  | them in this file.
  |
  */

  /*
  Only show the mobile number field if the notification type is set to Text. This function will be expanded
  as more notification types are added to the app.
  */
  var notificationType = document.getElementsByName("notificationType")[0];
  if (notificationType){
    var mNumInput = document.getElementsByName("mobileNumber")[0];
    var mNumDiv = document.querySelector("#mobileNumber");

    if (notificationType.value == "T"){
      mNumDiv.classList.remove("hidden");
      mNumInput.required = true;
    }
    else{
      mNumDiv.classList.add("hidden");
      mNumInput.required = false;
      mNumInput.setAttribute("value", "-1");
    }
  
    notificationType.addEventListener('change', function(event){
        if (notificationType.value == "T"){
            
          mNumDiv.classList.remove("hidden");
          mNumInput.required = true;
          if (mNumInput.getAttribute('value') === "-1"){
            mNumInput.setAttribute('value', "");
          }
        }
        else{
          mNumDiv.classList.add("hidden");
          mNumInput.required = false;
          if (mNumInput.getAttribute('value') === ""){
            mNumInput.setAttribute('value', "-1");
          }
        }
    })
  }

  /*
  First we check if the timezone id is present, this way we only auto set the timezone when a user is
  creating their profile. We then set timezone to the select element. Then we find the timezone and set
  it to the proper value base on the users timezone.
  */
  var timezone = document.getElementById("timezone");
  if  (timezone){
    timezone = document.getElementsByName("timezone")[0];
    var tz = getTimezoneName();
    var options = timezone.options;
    for (var i=0; i<options.length;i++) {
      if (options[i].value === tz){
        options[i].selected = true;
        break;
      }
    }
  }

  function getTimezoneName() {
    var tmSummer = new Date(Date.UTC(2005, 6, 30, 0, 0, 0, 0));
    var so = -1 * tmSummer.getTimezoneOffset();
    var tmWinter = new Date(Date.UTC(2005, 12, 30, 0, 0, 0, 0));
    var wo = -1 * tmWinter.getTimezoneOffset();
  
    if (-660 == so && -660 == wo) return 'Pacific/Midway';
    if (-600 == so && -600 == wo) return 'Pacific/Tahiti';
    if (-570 == so && -570 == wo) return 'Pacific/Marquesas';
    if (-540 == so && -600 == wo) return 'America/Adak';
    if (-540 == so && -540 == wo) return 'Pacific/Gambier';
    if (-480 == so && -540 == wo) return 'US/Alaska';
    if (-480 == so && -480 == wo) return 'Pacific/Pitcairn';
    if (-420 == so && -480 == wo) return 'US/Pacific';
    if (-420 == so && -420 == wo) return 'US/Arizona';
    if (-360 == so && -420 == wo) return 'US/Mountain';
    if (-360 == so && -360 == wo) return 'America/Guatemala';
    if (-360 == so && -300 == wo) return 'Pacific/Easter';
    if (-300 == so && -360 == wo) return 'US/Central';
    if (-300 == so && -300 == wo) return 'America/Bogota';
    if (-240 == so && -300 == wo) return 'US/Eastern';
    if (-240 == so && -240 == wo) return 'America/Caracas';
    if (-240 == so && -180 == wo) return 'America/Santiago';
    if (-180 == so && -240 == wo) return 'Canada/Atlantic';
    if (-180 == so && -180 == wo) return 'America/Montevideo';
    if (-180 == so && -120 == wo) return 'America/Sao_Paulo';
    if (-150 == so && -210 == wo) return 'America/St_Johns';
    if (-120 == so && -180 == wo) return 'America/Godthab';
    if (-120 == so && -120 == wo) return 'America/Noronha';
    if (-60 == so && -60 == wo) return 'Atlantic/Cape_Verde';
    if (0 == so && -60 == wo) return 'Atlantic/Azores';
    if (0 == so && 0 == wo) return 'Africa/Casablanca';
    if (60 == so && 0 == wo) return 'Europe/London';
    if (60 == so && 60 == wo) return 'Africa/Algiers';
    if (60 == so && 120 == wo) return 'Africa/Windhoek';
    if (120 == so && 60 == wo) return 'Europe/Amsterdam';
    if (120 == so && 120 == wo) return 'Africa/Harare';
    if (180 == so && 120 == wo) return 'Europe/Athens';
    if (180 == so && 180 == wo) return 'Africa/Nairobi';
    if (240 == so && 180 == wo) return 'Europe/Moscow';
    if (240 == so && 240 == wo) return 'Asia/Dubai';
    if (270 == so && 210 == wo) return 'Asia/Tehran';
    if (270 == so && 270 == wo) return 'Asia/Kabul';
    if (300 == so && 240 == wo) return 'Asia/Baku';
    if (300 == so && 300 == wo) return 'Asia/Karachi';
    if (330 == so && 330 == wo) return 'Asia/Calcutta';
    if (345 == so && 345 == wo) return 'Asia/Katmandu';
    if (360 == so && 300 == wo) return 'Asia/Yekaterinburg';
    if (360 == so && 360 == wo) return 'Asia/Colombo';
    if (390 == so && 390 == wo) return 'Asia/Rangoon';
    if (420 == so && 360 == wo) return 'Asia/Almaty';
    if (420 == so && 420 == wo) return 'Asia/Bangkok';
    if (480 == so && 420 == wo) return 'Asia/Krasnoyarsk';
    if (480 == so && 480 == wo) return 'Australia/Perth';
    if (540 == so && 480 == wo) return 'Asia/Irkutsk';
    if (540 == so && 540 == wo) return 'Asia/Tokyo';
    if (570 == so && 570 == wo) return 'Australia/Darwin';
    if (570 == so && 630 == wo) return 'Australia/Adelaide';
    if (600 == so && 540 == wo) return 'Asia/Yakutsk';
    if (600 == so && 600 == wo) return 'Australia/Brisbane';
    if (600 == so && 660 == wo) return 'Australia/Sydney';
    if (630 == so && 660 == wo) return 'Australia/Lord_Howe';
    if (660 == so && 600 == wo) return 'Asia/Vladivostok';
    if (660 == so && 660 == wo) return 'Pacific/Guadalcanal';
    if (690 == so && 690 == wo) return 'Pacific/Norfolk';
    if (720 == so && 660 == wo) return 'Asia/Magadan';
    if (720 == so && 720 == wo) return 'Pacific/Fiji';
    if (720 == so && 780 == wo) return 'Pacific/Auckland';
    if (765 == so && 825 == wo) return 'Pacific/Chatham';
    if (780 == so && 780 == wo) return 'Pacific/Enderbury'
    if (840 == so && 840 == wo) return 'Pacific/Kiritimati';
    return 'US/Pacific';
  }
});

