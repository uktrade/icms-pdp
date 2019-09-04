import fontSpy from './thirdparty/fontspy-3.0.0'
import jQuery from './thirdparty/jquery-1.12.4'
import './thirdparty/jqueryui-1.12.1'
import './thirdparty/sticky-kit-1.1.2'
import './thirdparty/tool-tipster-4.2.5'
import './thirdparty/autosize-1.18.4'
import './thirdparty/jquery-timepicker-addon-1.5.0'

window.$ = window.jQuery = jQuery;

/*
 * FOX JS
 *
 * Copyright 2017, Fivium Ltd.
 * Released under the BSD 3-Clause license.
 *
 * Dependencies:
 *   jQuery v1.11
 *   jQuery-FontSpy v3
 *   Tooltipster v4.2.5
 */

// Can be run through JSDoc (https://github.com/jsdoc3/jsdoc) and JSHint (http://www.jshint.com/)

/*jshint laxcomma: true, laxbreak: true, strict: false */

var FOXjs = {
  gPageDisabled: false,
  gPageExpired: false,

  // Store a reason for why the page cannot be submitted
  gBlockSubmitReason: null,

  // Hold timers to clear later
  gTimers: {},

  // Array of client actions
  gClientActionQueue: [],

  /**
   * Get a cookie for a given name
   * @param {string} name The name of the cookie to get
   * @returns {string} The value stored in the cookie
   * @static
   */
  getCookie: function(name) {
    if (document.cookie.length > 0) {
      var begin = document.cookie.indexOf(name + "=");
      if (begin != -1) {
        begin += name.length + 1;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
          end = document.cookie.length;
        }
        return decodeURIComponent(document.cookie.substring(begin, end));
      }
    }
    return null;
  },

  /**
   * Set the value of a cookie, optionally specifying when to expire and a path the cookie should be available on
   * @param {string} name The name of the cookie to set
   * @param {string} value The value of the cookie
   * @param {int} expireDays How many days should the cookie last for
   * @param {string} path The path to scope access to this cookie to
   * @static
   */
  setCookie: function(name, value, expireDays, path) {
    var newCookie = name + "=" + encodeURI(value);
    if (expireDays !== null) {
      var expiresDateTime = new Date();
      expiresDateTime.setTime(expiresDateTime.getTime() + (expireDays * 24 * 3600 * 1000));
      newCookie += "; expires=" + expiresDateTime.toUTCString();
    }
    if (path !== null) {
      newCookie += "; path=" + path;
    }
    document.cookie = newCookie;
  },

  /**
   * Remove a cookie on the current domain which has a given name
   * @param {string} name The name of the cookie to remove
   * @static
   */
  removeCookie: function(name) {
    this.setCookie(name, "", -1, null);
  },

  /**
   * Initialise everything needed for a FOX page e.g. Scroll position, hint icons, calendars...
   * @param {function} successFunction Function to run when a page is successfully initialised
   */
  init: function(successFunction) {
    // Check icon font has loaded
    // Glyphs have to be ones that are more than 1em wide otherwise this doesn't work in IE
    fontSpy("icomoon", {glyphs: "\ue9be\ue90e\ue91b\ue920"});

    // Init sticky panels
    $( document ).ready(function(){$(".sticky").stick_in_parent({parent: '.container'});});

    //https://github.com/leafo/sticky-kit/issues/31
    $('.sticky')
    .on('sticky_kit:bottom', function(e) {
        $(this).parent().css('position', 'static');
    })
    .on('sticky_kit:unbottom', function(e) {
        $(this).parent().css('position', 'relative');
    });

    // Preserve scroll position
    // var scrollPosition = parseInt(document.mainForm.scroll_position.value);
    // if (scrollPosition > 0) {
      // window.scrollTo(0, scrollPosition);
    // }


    // Scroll to first error on the page after submit.
    var error = $("form .error-message");
    if(error.length > 0) {
      var row = error.first().closest('div[class="row"]');
      $('html, body').animate({
        scrollTop: (row.offset().top)
      },0);
    }

    // Prevent page presentation caching in browsers that support it
    $(window).on("unload", function () {
      // no body needed
    });

    // Set default properties for hint icons
    $.tooltipster.setDefaults({
      theme: "tooltipster-foxopen",
      contentAsHTML: true,
      delay: 0,
      animationDuration: 100,
      side: "bottom",
      maxWidth: 250
    });

    // Enable hints on focus of elements with hint icons, rather than requiring hovering the icon
    $("[data-hint-id]").on({
      focus: function() {
        $("#" + $(this).data("hint-id")).tooltipster("open");
      },
      blur: function() {
        $("#" + $(this).data("hint-id")).tooltipster("close");
      }
    });

    // Add tooltipster hooks to elements with hints/tooltips
    $(".hint, .tooltip").each(
        function() {
          FOXjs.addHintToTarget(this);
        }
    );

    // Enable autosize on textareas with the autosize data attribute
    $("textarea[data-auto-resize = 'true']").autosize();

    // Limit textarea length in <= IE9
    if (!("maxLength" in document.createElement("textarea"))) {
      $("textarea[maxlength]").on('keyup blur paste drop', function () {
        var that = $(this);
        //setTimeout required so the browser has time to see the pasted value in a paste event
        setTimeout(function() {
          var maxLength = that.attr('maxlength');
          var val = that.val();

          if (val.length > maxLength) {
            that.val(val.slice(0, maxLength));
          }
        }, 0);
      });
    }

    // Initialise the date pickers for fields that need them
    $( ".date-input").not(".date-time-input").not("[readonly='readonly']").datepicker({
      changeMonth: true,
      changeYear: true,
      dateFormat: "dd'-'M'-'yy",
      showButtonPanel: true,
      yearRange: "c-100:c+100"
    });
    $( ".date-time-input" ).not('[readonly="readonly"]').datetimepicker({
      controlType: $.timepicker.textTimeControl,
      changeMonth: true,
      changeYear: true,
      dateFormat: "dd'-'M'-'yy",
      showButtonPanel: true,
      yearRange: "c-100:c+100"
    });
    $( ".date-icon").click(function(){
      var inputId = '#' + $(this).attr("id").replace("icon","");
      if($(inputId).datepicker( "widget" ).is(":visible")) {
        $(inputId).datepicker("hide");
      }
      else {
        $(inputId).datepicker("show");
      }
    });

    // Enable onchange attribute on selectors in a keyboard-accessible way
    this._overrideSelectorOnChange();

    // Enable focussing on tickboxes/radio buttons that have been styled like buttons
    this._enableTickboxButtonFocus();

    // Enable dropdown buttons
    FOXdropdowns.init();

    // Run page scripts or catch erroneous navigation
    // if (!this.isExpired()) {
    //   successFunction();

    //   // Trigger any blocks of code inside a $(document).on('foxReady', function(){ });
    //   $(document).trigger('foxReady');

    //   // Okay to give 'back' nav warning again
    //   this.removeCookie("backWarningGiven_" + document.mainForm.thread_id.value);

    //   this.allowSubmit();
    // }
    // else {
    //   this.erroneousNavigation();
    // }

  },

  /**
   * Add tooltip hint to a target element
   *
   * @param {object} targetElement Element to trigger the tooltip off
   * @param {string} hintContentID Optionally set the ID of the hint content element to make sure it's set on the target
   * @static
   */
  addHintToTarget: function(targetElement, hintContentID) {
    targetElement = $(targetElement);
    if (hintContentID) {
      // make sure the target element has an aria tag pointing to the content
      targetElement.attr('aria-describedby', hintContentID);
    }

    var hintContentElement = $('#' + targetElement.attr("aria-describedby"));
    targetElement.tooltipster({
      functionInit: function(instance, helper){
        instance.content(hintContentElement.html());
      },
      functionReady: function(instance, helper){
        hintContentElement.attr('aria-hidden', false);
      },
      functionAfter: function(instance, helper){
        hintContentElement.attr('aria-hidden', true);
      },
      interactive: (hintContentElement.find('a').length > 0)
    });
  },

  /**
   * Set up selector elements to deal with OnChange events in a more accessible way
   */
  _overrideSelectorOnChange: function() {
    /**
     * Handle onchange event for the selector
     *
     * @param theElement
     * @returns {boolean}
     */
    function selectChanged(theElement) {
      var theSelect;

      if (theElement && theElement.value) {
        theSelect = theElement;
      }
      else {
        theSelect = this;
      }

      // Return false if nothing was noted as being changed and the element wasn't turned into a tagger
      if (theSelect.suppressOnChange || (theSelect.value === theSelect.initValue && !$(theSelect).data('isTagger'))) {
        theSelect.suppressOnChange = false;
        return false;
      }

      // In IE, we get a warning that the form has been submitted twice if we fire the original onchange twice
      // (because selectChange gets triggered by onchange and by selectBlurred) so we set supressOnChange so
      // it doesn't get fired again
      theSelect.suppressOnChange = true;

      theSelect.originalonchange();

      return true;
    }

    /**
     * Handle the focus event by storing the original value so we can test later to see if it actually changed before
     * firing the onchange event
     * @returns {boolean}
     */
    function selectFocused() {
      if(!this.hasOwnProperty('initValue')) {
        this.initValue = this.value;
      }
      return true;
    }

    /**
     * Handle the blur event
     * @returns {boolean}
     */
    function selectBlurred() {
      selectChanged(this);
      return true;
    }

    /**
     * Handle keydown events
     * @param e
     * @returns {boolean}
     */
    function selectKeyed(e) {
      var theEvent;
      var keyCodeTab = 9; // Tab
      var keyCodeEnter = 13; // Enter
      var keyCodeEsc = 27; // Esc


      if (e) {
        theEvent = e;
      }
      else {
        theEvent = event;
      }

      if ((theEvent.keyCode === keyCodeEnter || theEvent.keyCode === keyCodeTab) && this.value !== this.initValue) {
        this.suppressOnChange = false;
        selectChanged(this);
      }
      else if (theEvent.keyCode === keyCodeEsc) {
        this.value = this.initValue;
      }

      this.suppressOnChange = true;

      return true;
    }

    $('select[onchange]').map(function(pIndex, pElement) {
      pElement.originalonchange = pElement.onchange;
      pElement.onfocus = selectFocused;
      pElement.onchange = selectChanged;
      pElement.onkeydown = selectKeyed;
      pElement.onblur = selectBlurred;
    });
  },

  /**
   * For tickboxes and radio buttons that have been styled like buttons, allow focusing on the label and pass the
   * click through to the input
   */
  _enableTickboxButtonFocus: function() {
    $('.button-option-label input').on('focus',function(){
      $(this).attr('tabindex','-1');
      $('label[for='+$(this).attr('id').replace('/','\\/')+']').attr('tabindex','0').focus();
    });

    $('.button-option-label label').on('blur',function(){
      $(this).removeAttr('tabindex');
      $('input[id='+$(this).attr('for').replace('/','\\/')+']').removeAttr('tabindex');
    });

    $('.button-option-label label').on('keydown', function(e){
      //Enter or Space
      if(e.keyCode==13 || e.keyCode==32) {
        $('input[id='+$(this).attr('for').replace('/','\\/')+']').click();
      }
    });
  },

  /**
   * Show an alert with information telling the user that because of their backwards navigation links will not work until
   * they navigate forwards again.
   */
  erroneousNavigation: function() {
    var cookieId = "backWarningGiven_" + document.mainForm.thread_id.value;
    this.setPageExpired(true);
    if (!FOXjs.getCookie(cookieId)) {
      FOXalert.textAlert("<p>To avoid losing data, please don't use your browser's Back button.</p><p>You can read or copy information from this page, but you'll need to go forward again to continue.</p>", {"alertStyle": "warning", "title":"Page expired"});
      // warn only on first back
      FOXjs.setCookie(cookieId, "true", 1, null);
    }
  },

  /**
   * Check to see if the page has "expired"
   * @private
   */
  isExpired: function() {
    // Get the cookie's raw value (decoded from URI encoding)
    var fieldSetCookie = this.getCookie("field_set");
    // Parse into an object
    var fieldSetArray = $.parseJSON(fieldSetCookie);
    // Loop through each item in the array and find the object with a matching thread id
    for(var i = 0; i < fieldSetArray.length; i++){
      // t = thread id, f = field set id
      if(document.mainForm.thread_id.value == fieldSetArray[i].t){
        return (fieldSetArray[i].f != document.mainForm.field_set.value);
      }
    }
    // This thread ID not found in cookie
    return false;
  },

  /**
   * Greys out page and marks it as expired if passed true
   * @param {boolean} isExpired Is the page expired
   * @private
   */
  setPageExpired: function(isExpired) {

    if (isExpired) {
      this.gPageExpired = true;
      $(document.body).addClass("disabled");
    }
    else {
      this.gPageExpired = false;
      $(document.body).removeClass("disabled");
    }
  },

  /**
   * Block out the page and "disable" it if passed true
   * @param {boolean} isDisabled Is the page disabled
   * @protected
   */
  setPageDisabled: function(isDisabled) {
    if (isDisabled == this.gPageDisabled) {
      return;
    }

    if (this.gPageExpired) {
      // Page shouldn't be expired and disabled
      this.setPageExpired(false);
    }

    if (isDisabled) {
      var blockingDiv = document.createElement("div");
      blockingDiv.setAttribute("id", "blocking-div");
      blockingDiv.style.height = document.body.scrollHeight;
      blockingDiv.style.width = document.body.scrollWidth;

      // Dynamically resize blocking div
      $(window).resize(function() {
        blockingDiv.style.height = document.body.scrollHeight;
        blockingDiv.style.width = document.body.scrollWidth;
      });

      document.body.appendChild(blockingDiv);
    }
    else {
      document.body.removeChild(document.getElementById("blocking-div"));
    }

    this.gPageDisabled = isDisabled;
  },

  /**
   * Display optional loading blocker when sending data to update
   * @private
   */
  showUpdating: function() {
    var updatingDiv = $("#updating");

    if (!updatingDiv) {
      // If no loading div on the page ignore this fucntion
      return;
    }

    updatingDiv.show();

    var blankingFrame = $("#iframe-wrapper");
    blankingFrame.show();

    $("img", updatingDiv).each(function() {
          // Update src URLs of images in the updating div so IE continues to run their animation
          this.src = this.src;
        }
    );

    document.body.style.cursor = "wait";

    this.setPageDisabled(true);

    window.setTimeout(function(){
      var closeButton = document.getElementById("updating-close-button");
      closeButton.style.visibility = "visible";
      closeButton.style.display = "block";
    }, 1000*60*5); // 5 minutes
    // Stop resubmission in IE
    if ("activeElement" in document && document.activeElement !== document.body) {
      document.activeElement.blur();
    }
    this.blockSubmit("The page is already loading. Please wait for the page to finish loading before performing further actions.");
  },

  /**
   * Run a server side action. Make sure the main form is up to date and post it.
   * @param {object} options Information about the action to run
   * @param {HTMLElement} [triggerElement] Element used to trigger the action
   */
  action: function(options, triggerElement) {
    var settings = $.extend({
      ref: null,
      ctxt: null,
      confirm: null,
      params: null
    }, options);

    if (settings.ref === null) {
      return; // Can't run an action without reference
    }

    var that = this;
    if (this.isExpired()) {
      // If the page has expired notify them
      var goForwardConfirm = "<p>It looks like you have navigated back to this page using the browser back button.</p> " +
        "<p>You will need to go forward to the most recent page before you can click any links or buttons.</p>" +
        "<p>Click <strong>OK</strong> to be taken to your most recent page.</p>" +
        "<p>Click <strong>Cancel</strong> to remain on this expired page.</p>";

      FOXalert.textConfirm(goForwardConfirm, {title: 'Page expired', alertStyle: 'warning'}, function() { that._expiredPageGoForward(settings); }, null);
    }
    else if (settings.confirm) {
      // Can't run an action if a confirm is defined and not okay'd by the user
      // Note if confirm fails, option widgets (selectors/tickboxes/radios) must be reset to their initial value
      FOXalert.textConfirm(settings.confirm, {}, function() { that._runAction(settings); },  function() { FOXoptions.resetToInitialValue(triggerElement); } );
    }
    else {
      this._runAction(settings);
    }
  },

  _runAction : function(settings) {

    if (this.gBlockSubmitReason !== null) {
      alert(this.gBlockSubmitReason);
    }
    else if (!this.gPageDisabled) {

      //Notify listeners that the form is about to be submitted, giving them a chance to set field values etc
      $(document).trigger('foxBeforeSubmit');

      // If the page is not disabled, set up some values and submit the form
      document.mainForm.scroll_position.value = Math.round($(document).scrollTop());
      document.mainForm.action_name.value = settings.ref;
      document.mainForm.context_ref.value = settings.ctxt;

      // Action params - write to JSON
      document.mainForm.action_params.value = JSON.stringify(settings.params);

      if(this.gClientActionQueue.length > 0) {
        $(document.mainForm).append($("<input type=\"hidden\" name=\"client_actions\"/>"));
        document.mainForm.client_actions.value = JSON.stringify(this.gClientActionQueue);
      }

      // Process HTMLArea code, or anything else pre-submit
      document.mainForm.onsubmit();

      // POST form
      document.mainForm.submit();

      // Show "loading/updating"
      this.showUpdating();
    }
  },

  _expiredPageGoForward : function() {
    // A bit ugly, but worst case scenario is that we go nowhere and user has to use browser forward button
    // If problematic, could add a form POST timeout to make sure users go somewhere

    // IE, Opera will go to top of history stack with this
    // assuming < 999 pages navigated
    for (var b = 999; b > 0; b--) {
      window.history.go(b);
    }

    // Firefox prefers this instead
    for (var f = 1; f <= 999; f++) {
      window.history.go(f);
    }
  },

  /**
   * Open popup windows
   * @param {object} options Information about the window to pop up
   */
  openwin: function(options) {
    var settings = $.extend({
      url: null
      , windowName: ""
      , windowOptions: "default"
      , windowProperties: ""
    }, options);

    if (settings.url) {
      settings.url = settings.url.replace(/&amp;/g,"&");

      switch (settings.windowOptions) {
        case "default":
          window.open(settings.url, settings.windowName, "");
          break;
        case "custom":
          window.open(settings.url, settings.windowName, settings.windowProperties);
          break;
        case "appwin":
          window.open(settings.url, settings.windowName, "toolbar=0,location=0,directories=0,status=1,menubar=0,scrollbars=1,resizable=1,left=0,top=0,width=" + (screen.availWidth-10) + ",height=" + (screen.availHeight-25));
          break;
        case "searchwin":
          window.open(settings.url, "searchwin", "toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=0,bgcolor=#003399,width=600,height=700,left=100,top=10");
          break;
        case "filewin":
          window.open(settings.url, "filewin", "toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1,bgcolor=#003399,width=1013,height=680,left=100,top=10");
          break;
        case "refwin":
          window.open(settings.url, "refwin", "toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1,bgcolor=#000066,width=800,height=600,left=100,top=75");
          break;
        case "helpwin":
          window.open(settings.url, "", "toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1,bgcolor=#003399,width=600,height=500,left=100,top=10");
          break;
        case "fullwin":
          window.open(settings.url, settings.windowName, "toolbar=1,location=1,directories=1,status=1,menubar=1,scrollbars=1,resizable=1,width=900,height=700,left=50,top=10");
          break;
        case "flushwin":
          window.open(settings.url, "flushwin", "toolbar=1,location=0,directories=0,status=0,menubar=1,scrollbars=1,resizable=1,width=638,height=105,left=100,top=100");
          break;
        default:
          window.open(settings.url, settings.windowName, "");
      }
    }
  },

  /**
   * Left pad string with paddingCharacter until string is resultLength long
   * @param {string} string String to add padding to
   * @param {string} resultLength Length of the string after padding
   * @param {string} paddingCharacter Character to pad with
   * @return {string} string padded with paddingCharacter until resultLength characters long
   */
  leftPad: function(string, resultLength, paddingCharacter) {
    string = string.toString();
    return string.length < resultLength ? this.leftPad(paddingCharacter + string, resultLength) : string;
  },

  /**
   * Run timer code for elements with a value of MM:SS with a callback at the deadline
   * @param {element} element Input field with a timeout defined in it with the format MM:SS
   * @param {function} callback Function to run after the timeout defined in element
   */
  startTimer: function(element, callback) {
    var that = this;
    this.gTimers[element.attr("id")] = setInterval(function() {
          var lTimeParts = element.val().split(':');
          var lMinutes = parseInt(lTimeParts[0]);
          var lSeconds = parseInt(lTimeParts[1]);
          if (lMinutes === 0 && lSeconds === 0) {
            // Bail out if there's no time on the clock to start with
            clearInterval(that.gTimers[element.attr('id')]);
            return;
          }
          else if (lSeconds === 0) {
            // If no seconds left, decrement the minutes and reset the seconds
            lMinutes--;
            lSeconds = "60";
          }

          lSeconds--;

          element.val(that.leftPad(lMinutes, 2, "0") + ":" + that.leftPad(lSeconds, 2, "0"));

          // If we just got to the deadline, clear this interval and run the action
          if (lMinutes === 0 && lSeconds === 0) {
            clearInterval(that.gTimers[element.attr("id")]);
            callback();
          }
        }
        , 1000);
  },

  /**
   * Mark the page as non-submittable, i.e. no actions should be run, with a reason
   * @param {string} reason Reason why the page cannot be submitted currently
   * @private
   */
  blockSubmit: function(reason) {
    this.gBlockSubmitReason = reason;
  },

  /**
   * Mark the page as submittable, clearing any previous blockage reason
   * @private
   */
  allowSubmit: function() {
    this.gBlockSubmitReason = null;
  },

  /**
   * Move focus to an element with an optional Y offset
   * @param {string} externalFoxId Value of a data-xfid on one or more elements
   * @param {int} yOffset Vertical offset, should you want the page to show information above/below the targeted elements
   */
  focus: function(externalFoxId, yOffset) {
    var lFocusTargets = $("*[data-xfid=" + externalFoxId + "]");
    // Scroll document to focus position
    if(lFocusTargets.offset()) {
      $(document).scrollTop(lFocusTargets.offset().top + yOffset);
    }
    // Attempt to focus a focusable element
    // TODO PN this needs to be aware of element visibility (otherwise IE might have an error)
    var lFocusTargetElement = lFocusTargets.find("input, select, textarea").first();
    if (!lFocusTargetElement.is(":visible")) {
      lFocusTargetElement.triggerHandler('focus');
    }
    else {
      lFocusTargetElement.focus();
    }
  },

  /**
   * Record a client side action with a given actionType for processing by the thread as part of the post data
   * @param {string} actionType
   * @param {string} actionKey
   * @param {object} actionParams
   */
  enqueueClientAction: function(actionType, actionKey, actionParams) {
    this.gClientActionQueue.push({action_type: actionType, action_key: actionKey, action_params: actionParams});
  },

  /**
   * Get all stored client side actions for a given actionType
   * @param actionType
   * @returns {array}
   */
  dequeueClientActions: function(actionType) {
    var lPreservedQueue = [];
    var lDequeuedItems = [];

    while(this.gClientActionQueue.length > 0) {
      // Remove items from the front of the queue
      var lItem = this.gClientActionQueue.splice(0, 1)[0];
      if(lItem.action_type == actionType) {
        lDequeuedItems.push(lItem);
      }
      else {
        lPreservedQueue.push(lItem);
      }
    }

    // Replace the original queue with the preserved queue
    this.gClientActionQueue = lPreservedQueue;

    return lDequeuedItems;
  }
};



var FOXtabs = {
  switchTab: function(pTabGroupKey, pTabKey) {
    // Hide all tab content divs and just show the one with the selected key
    $("div[data-tab-group='" + pTabGroupKey + "']").hide();
    $("div[data-tab-group='" + pTabGroupKey + "'][data-tab-key='" + pTabKey + "']").show();

    // Remove the accessible hidden attribute from all tab content divs and re-apply it to the one with the selected key
    $("div[data-tab-group='" + pTabGroupKey + "']").attr("aria-hidden", "true");
    $("div[data-tab-group='" + pTabGroupKey + "'][data-tab-key='" + pTabKey + "']").attr("aria-hidden", "false");

    // Remove the current-tab class from all tab links and re-apply it to the one with the selected key
    $("ul[data-tab-group='" + pTabGroupKey + "'] > li").removeClass("current-tab");
    $("ul[data-tab-group='" + pTabGroupKey + "'] > li[data-tab-key='" + pTabKey + "']").addClass("current-tab");

    // Remove the accessible selected attribute from all tab links and re-apply it to the one with the selected key
    $("ul[data-tab-group='" + pTabGroupKey + "'] > li").attr("aria-selected", "false");
    $("ul[data-tab-group='" + pTabGroupKey + "'] > li[data-tab-key='" + pTabKey + "']").attr("aria-selected", "true");

    // Set the hidden input field to the selected key
    $("input[data-tab-group='" + pTabGroupKey + "']").val(pTabKey);
  }
};

/*
 Adapted from accessible-modal-dialog by gdkraus: https://github.com/gdkraus/accessible-modal-dialog

 ============================================
 License for Application
 ============================================

 This license is governed by United States copyright law, and with respect to matters
 of tort, contract, and other causes of action it is governed by North Carolina law,
 without regard to North Carolina choice of law provisions.  The forum for any dispute
 resolution shall be in Wake County, North Carolina.

 Redistribution and use in source and binary forms, with or without modification, are
 permitted provided that the following conditions are met:

 1. Redistributions of source code must retain the above copyright notice, this list
 of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright notice, this
 list of conditions and the following disclaimer in the documentation and/or other
 materials provided with the distribution.

 3. The name of the author may not be used to endorse or promote products derived from
 this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
 WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
 AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE
 LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 */

var AccessibleModal = {
  // jQuery formatted selector to search for focusable items
  focusableElementsString: "a[href], area[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), iframe, object, embed, *[tabindex], *[contenteditable]",

  /**
   * Prevents tab key presses from focusing on elements outside the given object.
   * @param obj {jQuery} Object to prevent tabbing out of (i.e. the modal container)
   * @param evt {event} Keypress event which has fired.
   */
  trapTabKey: function (obj, evt) {
    // get list of all children elements in given object
    var o = obj.find('*');

    // get list of focusable items
    var focusableItems = o.filter(this.focusableElementsString).filter(':visible');

    // get currently focused item
    var focusedItem = jQuery(':focus');

    // get the number of focusable items
    var numberOfFocusableItems = focusableItems.length;

    // get the index of the currently focused item
    var focusedItemIndex = focusableItems.index(focusedItem);

    if (focusedItemIndex == -1 || (!evt.shiftKey && focusedItemIndex == numberOfFocusableItems - 1)) {
      //If focused outside the modal, bring focus to first item
      //Or if tab is pressed without shift, and we are on the last item, wrap around to the first item
      focusableItems.get(0).focus();
      evt.preventDefault();
    }
    else if (evt.shiftKey && focusedItemIndex == 0) {
      //back tab and we're focused on first item - go to the last focusable item
      focusableItems.get(numberOfFocusableItems - 1).focus();
      evt.preventDefault();
    }
  }
};
var FOXmodal = {

  /** Current DisplayedModals, in stack order. */
  modalStack: [],

  /**
   * Handles any initialisation actions which need to be performed if the page has been rendered with a visible modal popover
   * in the HTML.
   */
  _handleWindowLoad: function() {
    var $engineModal = $('#engine-modal-popover');
    if ($engineModal.is(':visible')) {
      this._createDisplayedModal($engineModal, 'engine-internal', false, null);
    }
  },

  /**
   * Gets the modal currently underneath the top modal on the stack, or undefined if the stack contains 1 or 0 modals.
   * @returns {DisplayedModal}
   * @private
   */
  _underTopModal: function () {
    return this.modalStack[this.modalStack.length - 2];
  },

  _keyEventHandler: function(event) {

    if (event.which == 27 && FOXmodal.topModal() && FOXmodal.topModal().escapeAllowed) {
      //Escape key - dismiss top modal if allowed
      FOXmodal.dismissTopModal();
    }
    else if (event.which == 9) {
      //Tab key - prevent tabbing out of modal
      AccessibleModal.trapTabKey(FOXmodal.topModal().$containerDiv, event);
    }
  },

  _registerKeyListeners: function() {
    $(document).on('keydown', this._keyEventHandler);
  },

  _deregisterKeyListeners: function() {
    $(document).off('keydown', this._keyEventHandler);
  },

  /**
   * Constructs a DisplayedModal and adds it onto the stack.
   * @param {jQuery} $modalContainer Div containing the rendered modal.
   * @param {string} modalKey Key for the new modal.
   * @param {boolean} escapeAllowed True if an 'escape' keypress can close the modal.
   * @param {HTMLElement} restoreFocusTo DOM element to restore focus to on modal close.
   * @param {function} closeCallback Callback function to run when the modal is closed.
   */
  _createDisplayedModal: function($modalContainer, modalKey, escapeAllowed, restoreFocusTo, closeCallback) {
    this.modalStack.push(new DisplayedModal($modalContainer, modalKey, escapeAllowed, restoreFocusTo, closeCallback));
    if (this.modalStack.length == 1) {
      $('body').addClass('contains-popover');
      this._registerKeyListeners();
    }

    if (this.modalStack.length > 1) {
      //Ensure the z-index of the top modal is higher than the modal it is over
      this.topModal().$containerDiv.css("z-index", parseInt(this._underTopModal().$containerDiv.css("z-index") + 1));

      //Disallow scrolling in the modal which is now beneath the top modal
      this._underTopModal().$containerDiv.addClass('contains-popover');
    }
  },

  /**
   * Displays a modal popover on the screen, which blocks clicks to underlying content.
   * @param {jQuery} $modalContent jQuery for the container of the popover content. The contents of this target will be copied into a new modal div.
   * @param {string} modalKey Key to identify the new modal, used to prevent the same modal being displayed repeatedly.
   * @param {object} modalOptions Additional options for the modal - title, size, etc.
   * @param {function} closeCallback Callback function to run when the modal is closed. The callback may take an object
   * parameter to be passed from dismissTopModal().
   */
  displayModal: function($modalContent, modalKey, modalOptions, closeCallback) {

    //Short circuit out if there is already a modal with the sanme key in the stack
    var matchingKeys = $.grep(this.modalStack, function(displayedModal) {
      return displayedModal.modalKey === modalKey;
    });
    if (matchingKeys.length > 0) {
      return;
    }

    modalOptions = $.extend({
      title: '',
      cssClass: '',
      size: 'regular',
      dismissAllowed: false,
      escapeAllowed: false,
      ariaRole: 'dialog',
      icon: ''
    }, modalOptions);

    //Note: until we add full Mustache support this must be kept in sync with ModalPopover.mustache
    var $modalContainer = $('<div class="modal-popover-container"><div class="modal-popover"><div class="modal-popover-content"></div></div></div>');

    if (modalOptions.title) {
      $modalContainer.find('.modal-popover-content').append('<h2 id="modal-title-' + modalKey + '">' + modalOptions.title + '</h2>');
      $modalContainer.find('.modal-popover-content').attr('aria-labelledby', 'modal-title-' + modalKey);
      //TODO: aria-describedby, needs to be sensible
    }

    $modalContainer.find('.modal-popover').addClass(modalOptions.size + '-popover').addClass(modalOptions.cssClass);

    //Copy CLONED contents so they are not removed from the DOM when we dimsiss the modal div
    $modalContainer.find('.modal-popover-content').append($modalContent.contents().clone());

    $modalContainer.find('.modal-popover-icon').addClass(modalOptions.icon);

    //Accessibility role
    $modalContainer.find('.modal-popover-content').attr('role', modalOptions.ariaRole);

    //Add new modal container to the start of the page body
    $('body').prepend($modalContainer);

    //Add dismiss icon if client side dismiss is allowed
    if (modalOptions.dismissAllowed) {
      $modalContainer.find('.modal-popover-content').prepend('<div class="icon-cancel-circle modal-dismiss" tabindex="1"></div>');
      var that = this;
      $modalContainer.find('.modal-dismiss').click(function(){
        that.dismissTopModal();
      });
    }

    //Construct tracker object and add to stack
    this._createDisplayedModal($modalContainer, modalKey, modalOptions.escapeAllowed, document.activeElement, closeCallback);
  },

  /**
   * Gets the top modal currently on the stack, or undefined if the stack is empty.
   * @returns {DisplayedModal}
   */
  topModal: function() {
    return this.modalStack[this.modalStack.length - 1];
  },

  /**
   * Dismisses (closes) the top modal.
   * @param {Object} [callbackArgs] Arguments to pass to the callback function.
   */
  dismissTopModal: function(callbackArgs) {

    var topModal =  this.modalStack.pop();

    if(topModal) {
      topModal.$containerDiv.remove(); //Note: this will remove the engine modal div, so will need to be recreated
    }

    if(this.modalStack.length == 0) {
      $('body').removeClass('contains-popover');
      this._deregisterKeyListeners();
    }
    else {
      //Still a modal on the stack, make sure scrolling is now allowed in it
      this.topModal().$containerDiv.removeClass('contains-popover');
    }

    //If we popped a DisplayedModal, run close actions
    if(topModal) {
      //Restore focus to whatever had it before
      if(topModal.restoreFocusTo) {
        var focusTargetElement = $(topModal.restoreFocusTo);
        if (!focusTargetElement.is(":visible")) {
          focusTargetElement.triggerHandler('focus');
        }
        else {
          focusTargetElement.focus();
        }
      }

      //Run close callback function
      if(topModal.closeCallback) {
        topModal.closeCallback(callbackArgs);
      }
    }
  },

  /**
   * Updates the hidden scroll position field to the current scroll position of the internal engine modal, if it is on the stack.
   */
  updateScrollPositionInput: function() {

    for (var i=0; i < this.modalStack.length; i++) {
      if (this.modalStack[i].isInternal) {
        $("input[name='modal_scroll_position']").val(Math.round(this.modalStack[i].$containerDiv.scrollTop()));
      }
    }
  },

  /**
   * Gets the jQuery object containing the currently displayed modal, or undefined if no modal is displayed.
   * @returns {jQuery}
   */
  getCurrentModalContainer: function() {
    return this.topModal().$containerDiv;
  }

};

/**
 * Creates a new DisplayedModal object which can be tracked by the FOXModal stack.
 * @param {jQuery} containerDiv element for the rendered modal
 * @param {string} modalKey key for the new modal.
 * @param {boolean} escapeAllowed True if an 'escape' keypress can close the modal.
 * @param {HTMLElement} restoreFocusTo DOM element to restore focus to on modal close.
 * @param {function} closeCallback Callback function to run when this modal is closed.
 * @constructor
 */
function DisplayedModal(containerDiv, modalKey, escapeAllowed, restoreFocusTo, closeCallback) {

  this.$containerDiv = containerDiv;
  this.modalKey = modalKey;
  this.isInternal = modalKey == 'engine-internal';
  this.escapeAllowed = escapeAllowed;
  this.restoreFocusTo = restoreFocusTo;
  this.closeCallback = closeCallback;

  if (this.isInternal && this.$containerDiv.data('initial-scroll-position')) {
    this.$containerDiv.scrollTop(this.$containerDiv.data('initial-scroll-position'));
    this.lastScrollTop = this.$containerDiv.scrollTop();
  }

  this.$containerDiv.on('scroll', function(e) {
    FOXmodal.topModal().updateDatePickerScrollPosition(e);
  })
}

DisplayedModal.prototype = {
  $containerDiv: null,
  modalKey: null,
  isInternal: false,
  escapeAllowed: false,
  restoreFocusTo: null,
  closeCallback: null,
  lastScrollTop: null,
  updateDatePickerScrollPosition: function(e) {
    var newTop = parseFloat($('#ui-datepicker-div').css('top')) - ( e.target.scrollTop - this.lastScrollTop);
    $('#ui-datepicker-div').css('top', newTop + 'px');
    this.lastScrollTop = e.target.scrollTop;
  }
};

//Modal event listeners

$(document).on('foxBeforeSubmit', function() {
  FOXmodal.updateScrollPositionInput();
});

$(document).ready(function() {
  FOXmodal._handleWindowLoad();
});

var FOXalert = {

  onLoadAlertQueue: [],

  alertCount: 0,

  /**
   * Gets a jQuery of HTML for an alert close button.
   * @param closePrompt
   * @returns {jQuery}
   * @private
   */
  _getAlertCloseControl: function(closePrompt) {
    return $('<ul class="modal-popover-actions"><li><button class="primary-button alert-dismiss" onclick="FOXmodal.dismissTopModal(); return false;">' + closePrompt + '</button></li></ul>');
  },

  /**
   * Gets a jQuery of HTML for an confirm "OK" and "Cancel" button.
   * @returns {jQuery}
   * @private
   */
  _getConfirmCloseControl: function() {
    return $('<ul class="modal-popover-actions">' +
      '<li><button class="primary-button alert-dismiss" onclick="FOXmodal.dismissTopModal({confirmResult: true}); return false;">OK</button></li>' +
      '<li><button class="link-button" onclick="FOXmodal.dismissTopModal({confirmResult: false}); return false;">Cancel</button></li></ul>');
  },

  /**
   * Gets an object containing styling properties to apply to an alert modal.
   * @param alertStyle Alert style enum.
   * @returns {{cssClass: string, icon: string}}
   * @private
   */
  _getAlertStyleData: function(alertStyle) {

    var result = {cssClass: 'modal-alert-' + alertStyle, icon: ''};

    switch (alertStyle) {
      case 'info':
        result.icon = 'icon-info'; break;
      case 'success':
        result.icon = 'icon-checkmark'; break;
      case 'warning':
        result.icon = 'icon-warning'; break;
      case 'danger':
        result.icon = 'icon-cross'; break;
      case 'confirm':
        result.icon = 'icon-question'; break;
    }

    return result;
  },

  /**
   * Displays an alert using FOXmodal.
   * @param $alertContent Alert content locator.
   * @param alertProperties Modal properties.
   * @param callback Callback to run on alert close.
   * @private
   */
  _displayAlert: function($alertContent, alertProperties, callback) {

    alertProperties = $.extend({
      size: 'small',
      alertStyle: 'normal',
      title: 'Alert',
      ariaRole: 'alertdialog',
      escapeAllowed: true,
      closePrompt: 'OK',
      isConfirm: false
    }, alertProperties);

    var alertKey = 'FOXalert' + (this.alertCount++);

    //Add close controls to the content container
    if (alertProperties.isConfirm) {
      $alertContent.append(this._getConfirmCloseControl());
    }
    else {
      $alertContent.append(this._getAlertCloseControl(alertProperties.closePrompt));
    }

    //Resolve alertStyle enum to icon/CSS classes
    var styleData = this._getAlertStyleData(alertProperties.alertStyle);

    alertProperties.cssClass = (alertProperties.cssClass ? alertProperties.cssClass + ' ' : '') + styleData.cssClass;
    alertProperties.icon = styleData.icon;

    //Show the modal
    FOXmodal.displayModal($alertContent, alertKey, alertProperties, callback);

    //Default focus on close action
    FOXmodal.getCurrentModalContainer().find('.alert-dismiss').focus();
  },

  /**
   * Displays a text-based alert.
   * @param alertText Alert text, which may contain HTML tags.
   * @param alertProperties Additional properties for the alert.
   * @param callback Callback to run on alert close.
   */
  textAlert: function(alertText, alertProperties, callback) {
    this._displayAlert($('<div><div class="modal-popover-icon"></div><div class="modal-popover-text">' + alertText +'</div></div>'), alertProperties, callback);
  },

  /**
   * Displays an alert with the contents of the given buffer.
   * @param $buffer Buffer locator.
   * @param alertProperties Additional properties for the alert.
   * @param callback Callback to run on alert close.
   */
  bufferAlert: function($buffer, alertProperties, callback) {
    this._displayAlert($buffer, alertProperties, callback);
  },

  /**
   * Displays a text-based confirm dialog.
   * @param confirmText Text of the confirm message.
   * @param confirmProperties Properties to pass to alert/modal functions.
   * @param successCallback Callback to run if the user clicks "OK".
   * @param cancelCallback Callback to run if the user clicks "Cancel".
   */
  textConfirm: function(confirmText, confirmProperties, successCallback, cancelCallback) {

    var callback = function(callbackResult) {
      if (callbackResult && callbackResult.confirmResult && successCallback) {
        successCallback();
      }
      else if (callbackResult && !callbackResult.confirmResult && cancelCallback) {
        cancelCallback();
      }
    };

    confirmProperties = $.extend({isConfirm: true, title: '', alertStyle: 'confirm'}, confirmProperties);

    this.textAlert(confirmText, confirmProperties, callback);
  },

  /**
   * Enqueues an alert for display when the page onLoad event fires.
   * @param alertProperties All alert properties, including message and alertType.
   */
  enqueueOnLoadAlert: function(alertProperties) {
    this.onLoadAlertQueue.push(alertProperties);
  },

  /**
   * Displays the next alert in the onLoad queue, if one exists.
   */
  processNextOnLoadAlert: function() {

    var alertProperties = this.onLoadAlertQueue.shift();
    if (alertProperties) {

      var that = this;
      var callback = function() { that.processNextOnLoadAlert(); };

      //Note callback chaining so only one alert is displayed at a time

      switch (alertProperties.alertType) {
        case 'native':
          //Convert newline strings to actual newlines (legacy behaviour migrated from HTML generator escaping logic)
          alert(alertProperties.message.replace(/\\n/g,'\n'));
          this.processNextOnLoadAlert();
          break;
        case 'text':
          this.textAlert(alertProperties.message, alertProperties, callback);
          break;
        case 'buffer':
          this.bufferAlert($('#' + alertProperties.bufferId), alertProperties, callback);
          break;
        default:
          throw 'Unknown alert type ' + alertProperties.alertType;
      }
    }
  }
};

/*
 * FOX Flash
 *
 * Copyright 2016, Fivium Ltd.
 * Released under the BSD 3-Clause license.
 *
 * Dependencies:
 *   jQuery v1.11
 */

// Can be run through JSDoc (https://github.com/jsdoc3/jsdoc) and JSHint (http://www.jshint.com/)

/*jshint laxcomma: true, laxbreak: true, strict: false */

var FOXflash = {

  /**
   * Gets a jQuery pointing to the container div for flash messages, creating it if it doesn't exist.
   * @returns {jQuery}
   * @private
   */
  _$getFlashContainer : function() {
    var container = $('.flash-message');
    if(container.length === 0) {
      container = $('<div class="flash-message"></div>').prependTo($(document.body));
      $('.flash-message').hide();
    }

    return container;
  },

  /**
   * Creates a flash div in the correct location.
   * @param message Message to display - may contain HTML for formatting.
   * @param infoBoxClass CSS classes to set on the div.
   * @private
   */
  _insertFlashHTML : function(message, infoBoxClass) {
    var flashContainer = this._$getFlashContainer();
    flashContainer.append('<div role="alert" class="info-box info-box-' + infoBoxClass + '" tabindex="0">' +
      '<button class="flash-message-close icon-cross" aria-label="Close this message">' +
    '</button>' + message +'</div>');
    flashContainer.find('.flash-message-close').click(function() { $(this).parent().fadeOut(100); });
    flashContainer.delay(200).fadeIn(300);
    // The focus has to happen once the element is visible, 500ms should be when it's fully visible
    setTimeout(function() {
      if ($(document.activeElement).parents('.flash-message').length === 0) {
        // Only focus the first child in the flash message container if the active element isn't already something in the flash message container
        flashContainer.children().first().focus();
      }
    }, 500);
  },

  /**
   * Displays a non-modal, text-based flash message at the top of the screen.
   * @param {string} message Message to display - may contain HTML for formatting.
   * @param {Object} flashProperties Additional properties such as style rules for the flash.
   */
  textFlash : function(message, flashProperties) {
    flashProperties = $.extend({
      displayType : 'info',
      cssClass: ''
    }, flashProperties);

    this._insertFlashHTML(message, flashProperties.displayType + ' ' + flashProperties.cssClass);
  }
};
/**
 * Controls for option widgets (selects, tickboxes, radios, etc)
 */
var FOXoptions = {

  /**
   * Records the initial values for option widgets in data attributes.
   */
  registerInitialValues: function() {
    //Record initial values of option widgets
    $('select, input[type="radio"], input[type="checkbox"]').each(function(i, e) {
      var value;
      var $element = $(e);
      if ($element.is('select')) {
        value = $element.val();
      }
      else {
        value = $element.prop('checked');
      }

      $element.data('fox-initial-value', value);
    });
  },

  /**
   * Resets the given element to its original value recorded in registerInitialValues.
   * @param resetTarget HTMLElement - a radio, tickbox or selector element.
   */
  resetToInitialValue: function(resetTarget) {
    var $target = $(resetTarget);
    if ($target.is('select')) {
      //If the element is a select, reset the value (this may be an array for multi selects)
      $target.val($target.data('fox-initial-value'));
    }
    else if ($target.is('input')) {
      if ($target.attr('type') === 'radio') {
        //Changing one radio will usually change another indirectly so we must reset them all
        $('input[name="' + $target.attr('name') + '"]').each(function (i, e) {
          $(e).prop('checked', $(e).data('fox-initial-value'));
        });
      }
      else if ($target.attr('type') === 'checkbox') {
        //For checkboxes, we only need to reset the current element
        $target.prop('checked', $target.data('fox-initial-value'));
      }
    }
  }
};

$(document).ready(function() { FOXoptions.registerInitialValues(); });
/*
 * FOX Dropdown Buttons
 *
 * Copyright 2017, Fivium Ltd.
 * Released under the BSD 3-Clause license.
 */

// Can be run through JSDoc (https://github.com/jsdoc3/jsdoc) and JSHint (http://www.jshint.com/)

/*jshint laxcomma: true, laxbreak: true, strict: false */
var FOXdropdowns = {

  /**
   * Toggles a dropdown's visiblity
   * @param {object} clickTarget The DOM element (button) that's been clicked
   * @private
   */
  _toggle: function(clickTarget) {
    // Record whether the one that was just clicked was already open, before we collapse them all
    var targetAlreadyExpanded = $(clickTarget).attr('aria-expanded') === 'true';

    // Collapse all dropdowns on page
    FOXdropdowns._hideAll();

    // Open the one that was clicked if it wasn't already open
    if(!targetAlreadyExpanded) {
      $(clickTarget).attr('aria-expanded',  'true');

      // Position the dropdown
      // Reset position first
      var $ul = $(clickTarget).siblings('ul');
      $ul.css('left', $(clickTarget).css('margin-left')).css('right','auto');

      $ul.show();

      var windowWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
      var ulWidth = parseFloat($ul.css('width'));
      var ulLeft = $ul.offset().left;

      // If the dropdown would go off the right edge of the screen, align it to the right edge of the button
      // instead of the left edge
      if(ulWidth + ulLeft > windowWidth) {
        $ul.css('left','auto').css('right', $(clickTarget).css('margin-right'));
      }

      // Position the dropdown below the bottom of the button
      var newTop = $(clickTarget).height() + parseFloat( $(clickTarget).css('padding-top')) + parseFloat( $(clickTarget).css('padding-bottom')) + 5 + 'px';
      $ul.css('top', newTop);
    }
  },

  /**
   * Hides all dropdown menus on the page
   * @private
   */
  _hideAll: function() {
    $('.dropdown-button').attr('aria-expanded', 'false').siblings('ul').hide();
  },

  /**
   * Initialises event handlers for dropdown buttons
   */
  init: function() {
    $('body').on('click', '.dropdown-button', function(e) {
      FOXdropdowns._toggle(e.target);
    });

    // Hide dropdowns when clicking or focussing anything that's not the currently open dropdown
    $('body').on('click', function(e) {
      // If the click isn't on a dropdown or one of its children (one of the list items), hide all dropdowns
      if($(e.target).closest('.dropdown-menu-out').length === 0) {
        FOXdropdowns._hideAll();
        e.stopPropagation();
      }
    });

    $('body').on('focus', '*', function(e) {
      // If the element with focus isn't inside the currently expanded dropdown, hide all dropdowns
      if($(e.target).closest('.dropdown-menu-out').find('.dropdown-button[aria-expanded=true]').length === 0) {
        FOXdropdowns._hideAll();
        e.stopPropagation();
      }
    });
  }
};
/*jshint laxcomma: true, laxbreak: true, strict: false */

var FOXdownloadBar = {

  showDownloadBar: function (params) {

    this._closeDownloadBar(); // Close in case its already open.
    this._buildDiv(params);

  },

  _buildDiv: function (params) {

    var containerDiv = $('<div id="foxDownloadBar">' +
      '<span id="downloadBarPromptSpan" class="icon-download"> </span>' +
      '</div>');

    if(params.isLocalTargetEnabled === true) {
      var localDownloadButton = $('<button id="downloadBarDownloadButton" class="button small-button icon-download">Download</button>');
      localDownloadButton.click(function () {document.location=params.downloadUrl; FOXdownloadBar. _closeDownloadBar();});
      containerDiv.append(localDownloadButton);
    }
    if(params.isGoogleDriveTargetEnabled === true) {
      var googleDriveButton = $('<button id="downloadBarSaveToDrive" class="button small-button icon-google-drive">Save to Google Drive</button>');
      googleDriveButton.click(function () {FOXdownloadBar._saveToDrive(params);});
      containerDiv.append(googleDriveButton);
    }

    containerDiv.append($('<span id="downloadBarStatusSpan" class="icon-animated-spinner"> </span>'));
    containerDiv.append($('<a id="downloadBarClose" href="#" class="icon-cross" title="Close" aria-label="Close download bar"> </a>'));

    var prompt;
    // Fox defaults to the filename 'file' if no filename was specified in some cases.
    if (!params.fileName || params.fileName === 'file') {
      prompt = 'What do you want to do with this file?';
    }
    else {
      prompt = 'What do you want to do with: ' + params.fileName + '?';
    }

    containerDiv.children('#downloadBarPromptSpan').text(prompt);

    // Return false here to stop the browser scrolling to the top of the page when clicking the a tag.
    containerDiv.children('#downloadBarClose').click( function () {FOXdownloadBar._closeDownloadBar(); return false;});

    $(document.body).append(containerDiv);

  },

  _saveToDrive: function (params) {
    $('#foxDownloadBar').find('> button').attr('disabled', true);
    $('#downloadBarStatusSpan').show().text('Saving to Google Drive');
    GoogleOauthProvider.initGoogleAuthInstance('https://www.googleapis.com/auth/drive.file', function () {FOXdownloadBar._googleAuthCallback(params);});
  },

  _googleAuthCallback: function (params) {

    var targetDownloadUrl = params.downloadUrl;
    var postData = [
      {name: "streamTarget", value: "GOOGLE_DRIVE"},
      {name: "accessToken", value: GoogleOauthProvider.getOauthAccessToken()}
    ];

    $.post(targetDownloadUrl, postData)
      .done(FOXdownloadBar._saveToDriveSuccessCallback)
      .fail(FOXdownloadBar._saveToDriveFailCallback);
  },

  _saveToDriveSuccessCallback: function (data, textStatus, jqXHR) {
    window.open(data, '_blank');
    FOXdownloadBar._closeDownloadBar();
  },

  _saveToDriveFailCallback: function (jqXHR, textStatus, errorThrown) {
    $('#downloadBarPromptSpan').remove();
    $('#foxDownloadBar').find('> button').remove();
    $('#downloadBarStatusSpan').removeClass('icon-animated-spinner').addClass('icon-cross').text('An error occurred when saving the file to Google Drive.');
  },

  _closeDownloadBar: function () {
    $('#foxDownloadBar').remove();
  }

};/*jshint laxcomma: true, laxbreak: true, strict: false */

var GoogleOauthProvider = {

  // The single instance of the google authorisation object. The auth2 can only be initialised once, so we manage the object here.
  _googleAuth: null,
  _clientId: null,

  _setClientId: function (clientId) {
    this._clientId = clientId;
  },

  _initGoogleAPIs: function (scope, callback) {
    var _this = this;
    if(!this.isGoogleDriveApiLoadStarted) {
      this.isGoogleDriveApiLoadStarted = true;
      // Load the Google Oauth APIs
      gapi.load('auth2:picker', {'callback': function () {
        //_this.isGoogleDriveApiLoadComplete = true;
        _this._initGoogleDriveAuth(scope, callback);
      }});
    }
  },

  _initGoogleDriveAuth: function (scope, callback) {
    var _this = this;
    // Initialise the OAuth2 context.
    gapi.auth2.init(
      {
        'client_id': _this._clientId,
        'scope': scope,
        'fetch_basic_profile': false // We don't need their profile information.
      }
    ).then(function () {
      // Set the GoogleAuth object now its been initialised.
      _this._googleAuth = gapi.auth2.getAuthInstance();

      // Request the user to sign in if they are not already
      if(_this._googleAuth.currentUser.get().isSignedIn()) {
        callback();
      }
      else {
        _this._googleAuth.signIn().then(callback);
      }

    }, function (error) {
      // Initialisation can fail if local storage or 3rd party cookies are disabled. The main culprit of this seems to be IE InPrivate mode.
      alert('An error occurred while loading Google Drive. If you are using InPrivate browsing in Internet Explorer, please disable InPrivate mode and load the page again.');
    });

  },

  /**
   * Initialises the Google Auth object instance, running the provided callback function once initialisation is complete.
   * The provided Google scope is guaranteed to be set, although other scopes may also be set.
   *
   * Once this is called, consumers can get an OAuth access token valid for the provided scope for the current user by
   * calling getOauthAccessToken();
   *
   * If initialisation fails the callback is not run.
   *
   * @param scope The scope needing to be authorised.
   * @param callback A function which is run on successful initialisation.
   */
  initGoogleAuthInstance: function (scope, callback) {

    // Check if the auth object is already initialised
    if(this._googleAuth !== null) {

      // Check if the user is logged in
      if(this._googleAuth.currentUser.get().isSignedIn()) {

        // User is logged in. Do they have the requested scope?
        var scopes = this._googleAuth.currentUser.get().getGrantedScopes().split(" ");
        if (scopes.indexOf(scope) > -1) {
          // They have the scope. Nothing needs to be done.
          callback();
        }
        else {
          // User is signed in, but doesn't have that scope. Request the scope
          this._googleAuth.currentUser.get().grant({'scope': scope}).then(callback);
        }
      }
      else {
        // User is not logged in. Sign in and request that scope in case they don't have it
        this._googleAuth.signIn({'scope': scope}).then(callback);
      }

    }
    else {
      // Initialise the auth object
      this._initGoogleAPIs(scope, callback);
    }
  },

  /**
   * Returns an OAuth access token for the current initialised scope(s) authorised by the current user.
   * initGoogleAuthInstance() MUST be called first to specify the required scope before calling this function. It is the
   * consumers responsibility to do this.
   *
   * @returns {string} The OAuth access token.
   */
  getOauthAccessToken: function() {
    return this._googleAuth.currentUser.get().getAuthResponse().access_token;
  }

};

$.timepicker.textTimeControl = {
  create: function(tp_inst, obj, unit, val, min, max, step){

    if ((val+"").length === 1) {
      val = '0'+val;
    }

    var input = '<input value="'+val+'" style="width:50%"/>';

    $(input).appendTo(obj).change(function (e) {
      var $t = obj.children('input');

      if ($t.val().length === 0) {
        $t.val('00');
      } else if ($t.val().length === 1) {
        $t.val('0'+$t.val())
      }

      tp_inst._onTimeChange();
      tp_inst._onSelectHandler();
    }).keypress(function (e) {
      //http://stackoverflow.com/questions/891696/jquery-what-is-the-best-way-to-restrict-number-only-input-for-textboxes-all
      // Backspace, tab, enter, end, home, left, right
      // We don't support the del key in Opera because del == . == 46.
      var controlKeys = [8, 9, 13, 35, 36, 37, 39];
      // IE doesn't support indexOf
      var isControlKey = controlKeys.join(",").match(new RegExp(event.which));
      // Some browsers just don't raise events for control keys. Easy.
      // e.g. Safari backspace.
      if (!event.which || // Control keys in most browsers. e.g. Firefox tab is 0
        (49 <= event.which && event.which <= 57) || // Always 1 through 9
        (48 == event.which && $(this).attr("value")) || // No 0 first digit
        isControlKey) { // Opera assigns values for control keys.
        return;
      } else {
        event.preventDefault();
      }
    });

    return obj;
  },
  options: function(tp_inst, obj, unit, opts, val){
    return null;
  },
  value: function(tp_inst, obj, unit, val){
    var $t = obj.children('input');
    if (val !== undefined) {
      return $t.val(val);
    }
    return $t.val();
  }
};



export default FOXjs;