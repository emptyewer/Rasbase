/**
 * Created by piperlab on 3/17/17.
 */
(function() {

  var f = [];
  f.csrfmiddlewaretoken = csrftoken;

  function $id(id) {
      return document.getElementById(id);
  }

  function formatBytes(bytes,decimals) {
     if(bytes == 0) return '0 Bytes';
     var k = 1000,
         dm = decimals + 1 || 3,
         sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
         i = Math.floor(Math.log(bytes) / Math.log(k));
     return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  function FileDragHover(e) {
      e.stopPropagation();
      e.preventDefault();
  }


  function ShowFileInfo(file) {
    $("#filelist").show();
    var text = "<div class='alert alert-warning'>" +
    "File: <strong>" + file.name +
          "</strong> of type: <strong>" + file.type +
          "</strong> size: <strong>" + formatBytes(file.size) +
          "</strong>" + "</div>";
    $("#list").append(text);
  }

  // file selection
  function FileDropHandler(e) {
    // cancel event and hover styling
    FileDragHover(e);
    // fetch FileList object
    var files = e.dataTransfer.files;
    if (files[0].type == "application/json") {
      ShowFileInfo(files[0]);
      f[files[0].name] = files[0];
    }
    else {
      // ShowFileInfo(files[0], 0);
      // RestoreHover();
    }
  }

  function CancelledHandler() {
      console.log("Cancelled");
      location.reload();
  }

  function UploadHandler(){
    $("#pbar").show();
    var data = new FormData();
    for (var key in f) {
      console.log(f[key]);
      data.append(key, f[key]);
    }
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

  function Init() {
      var filedrag = $id("drop_well");
      $id("cancel-button").addEventListener("click", CancelledHandler, false);
      $id("upload-button").addEventListener("click", UploadHandler, false);
      // is XHR2 available?
      var xhr = new XMLHttpRequest();
      if (xhr.upload) {
        // file drop
        filedrag.addEventListener("dragover", FileDragHover, false);
        filedrag.addEventListener("dragleave", FileDragHover, false);
        filedrag.addEventListener("drop", FileDropHandler, false);
        filedrag.style.display = "block";
        // remove submit button
        // submitbutton.style.display = "none";
      }
  }

  $(document).ready(function() {
    console.log(csrftoken);
    $("#pbar").hide();
    $("#filelist").hide();
    Init();
  });

})();
