/**
 * Created by piperlab on 2/23/17.
 */
var timer;                //timer identifier
var doneInterval = 5000;  //time in ms (5 seconds)

function validateForm() {
  var isValid = true;
  $('#metadata-form *').filter('input').each(function(){
    var $this = $(this);
    if ($this.val() == '') {
      isValid = false;
    }
  });

  $('#metadata-form *').filter('select').each(function(){
    var $this = $(this);
    if ($this.val() == 'Select') {
      isValid = false;
    }
  });
  return isValid;
}

//on keyup, start the countdown
$('#exp').keyup(function(){
    clearTimeout(timer);
    if ($('#exp').val()) {
        timer = setTimeout(done('#exp'), doneInterval);
    }
});

$("#bait").change(function () {
  clearTimeout(timer);
  if ($('#bait').val()) {
        timer = setTimeout(done('#bait'), doneInterval);
    }
});

$("#vector").change(function () {
  clearTimeout(timer);
  if ($('#vector').val()) {
        timer = setTimeout(done('#vector'), doneInterval);
    }
});

$("#library").change(function () {
  clearTimeout(timer);
  if ($('#library').val()) {
        timer = setTimeout(done('#library'), doneInterval);
    }
});

$("#reference").change(function () {
  clearTimeout(timer);
  if ($('#reference').val()) {
        timer = setTimeout(done('#reference'), doneInterval);
    }
});

$("#approval-button").click(function () {
  console.log(validateForm());
  if ( validateForm() == true) {
    $("table").faLoading('fa-cog');
    $("")
    $("#metadata-form").submit();
  }
  else {
    done('#exp');
    done('#bait');
    done('#vector');
    done('#library');
    done('#reference');
    $("#error-modal").modal('show');
  }
});

// $("#university").keyup(function () {
//   clearTimeout(timer);
//   if ($('#university').val()) {
//         timer = setTimeout(done('#university'), doneInterval);
//     }
// });
//
// $("#submitter").keyup(function () {
//   clearTimeout(timer);
//   if ($('#submitter').val()) {
//         timer = setTimeout(done('#submitter'), doneInterval);
//     }
// });


//user is "finished typing," do something
function done (id) {
    //do something
  if ($(id).prop('tagName') == 'INPUT') {
    if ($(id).val().length <= 0) {
      showError(id);
    }
    else {
      showSuccess(id);
    }
  }

  if ($(id).prop('tagName') == 'SELECT') {
    if ($(id).val() == 'Select') {
      showError(id);
    }
    else {
      showSuccess(id);
    }
  }
}

function showError(id) {
  $(id).parent().removeClass("has-success");
  $(id).parent().addClass("has-error");
}

function showSuccess(id) {
  $(id).parent().removeClass("has-error");
  $(id).parent().addClass("has-success");
}
