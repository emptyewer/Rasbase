


function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}

function validateForm() {
  var isValid = true;
  $('#upload-view select').each(
    function(index){
        var input = $(this);
        if (input.val() == 'Select') {
          isValid = false;
        }
    }
  );
  return isValid;
}

function disable_form_elements() {
  $("#upload-form input, #upload-form select, #upload-form label").attr('disabled',true);
}

var upload = function(event){
		console.log("Upload Clicked");
		event.preventDefault();
    var data = new FormData();
    for (var i = 0; i < fileinputs.length; i++) {
      var $parent = $(fileinputs[i].parentNode);
      console.log($parent[0].childNodes);
      if ($parent[0].childNodes.length > 4) {
        data.append(fileinputs[i].name + "_genome", $parent[0].getElementsByTagName("select").genome.value);
        data.append(fileinputs[i].name + "_prey", $parent[0].getElementsByTagName("select").prey.value);
      }
      if ($parent[0].childNodes.length == 7) {
        data.append(fileinputs[i].name + "_vector", $parent[0].getElementsByTagName("select").vector.value);
      }
      data.append(fileinputs[i].name, fileinputs[i].files[0]);
    }
    data.append('csrfmiddlewaretoken', csrftoken);
    console.log(validateForm());
    if ( validateForm() == true) {
      $("#pbar").show();
      _submit.disabled = true;
      disable_form_elements();
      $.ajax({
        url: 'upload',
        data: data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function(){
          $("#upload-view").fadeOut().hide();
          $("#success-notification").fadeIn().show();
        }
      });
    }
    else {
      highlight_invalid();
      $("#error-modal").modal('show');
    }
	};

function file_selected(event) {
  var $parent = $(event.target.parentNode);
  if (event.target.files.length == 1 && $parent[0].childElementCount == 2) {
    _submit.disabled = false;
    $parent.append("<div class='form-group input-group' style='padding-top: 15px'> <span class='input-group-addon'>Indexed Genome</span><select class='form-control' name='genome'><option>Select</option>" + genomes + "</select></div>");
      $parent.append("<div class='form-group input-group'> <span class='input-group-addon'>DEEPN Prey Library</span><select class='form-control' name='prey'><option>Select</option>" + preys + "</select></div>");
    if (event.target.id.match(/_bait.*/)) {
      $parent.append("<div class='form-group input-group'> <span class='input-group-addon'>Vector</span><select class='form-control' name='vector'><option>Select</option>" + vectors + "</select></div>");
    }
  }
}

function highlight_invalid () {
  $('#upload-view select').each(
    function(index){
        var input = $(this);
        if (input.val() == 'Select') {
          showError(input);
        }
        else {
          showSuccess(input)
        }
    }
  );
}

function showError(id) {
  $(id).parent().removeClass("has-success");
  $(id).parent().addClass("has-error");
}

function showSuccess(id) {
  $(id).parent().removeClass("has-error");
  $(id).parent().addClass("has-success");
}


$("#success-notification").hide();
$("#pbar").hide();

var _submit = document.getElementById('_submit'),
fileinputs = $('.filestyle');

fileinputs.each(function(){
  var $this = $(this);
  $this.change(file_selected)
});
_submit.disabled = true;
_submit.addEventListener('click', upload);
