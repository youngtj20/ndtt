'use strict';

$(document).ready(onLoad);

function onLoad() {
  $('label').on('keydown', onKeyDown);
}

function onKeyDown(e) {
  var enterKey = 13;
  var spaceKey = 32;
  if (e.keyCode === enterKey || e.keyCode === spaceKey) {
    $('#upload').click();
  }
}