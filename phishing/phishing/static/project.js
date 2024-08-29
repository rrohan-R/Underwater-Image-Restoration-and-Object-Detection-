var droppedFiles = false;
var fileName = '';
var $dropzone = $('.dropzone');
var $button = $('.upload-btn');
var uploading = false;
var $syncing = $('.syncing');
var $done = $('.done');
var $bar = $('.bar');
var timeOut;

$dropzone.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
	e.preventDefault();
	e.stopPropagation();
})
	.on('dragover dragenter', function() {
	$dropzone.addClass('is-dragover');
})
	.on('dragleave dragend drop', function() {
	$dropzone.removeClass('is-dragover');
})
	.on('drop', function(e) {
	droppedFiles = e.originalEvent.dataTransfer.files;
	fileName = droppedFiles[0]['name'];
	$('.filename').html(fileName);
	$('.dropzone .upload').hide();
});

$button.bind('click', function() {
	startUpload();
});

$("input:file").change(function (){
	fileName = $(this)[0].files[0].name;
	$('.filename').html(fileName);
	$('.dropzone .upload').hide();
});

function startUpload() {
	if (!uploading && fileName != '' ) {
		uploading = true;
		$button.html('Uploading...');
		$dropzone.fadeOut();
		$syncing.addClass('active');
		$done.addClass('active');
		$bar.addClass('active');
		timeoutID = window.setTimeout(showDone, 3200);
	}
}

function showDone() {
	$button.html('Done');
}

function readURL(input) {
	if (input.files && input.files[0]) {
		var reader = new FileReader();

		reader.onload = function (e) {
			if(input.files[0].type.indexOf("image")!=-1){
				$('.img-uploaded')
					.attr('src', e.target.result)
					.height(200);
					$('.sec-uploads').addClass('active');
			}
			else {
				alert("Invalid image. Please upload valid image file.");
				$('#formFileLg').val('');
				$('.sec-uploads').removeClass('active');
			}
		};

		reader.readAsDataURL(input.files[0]);
	}
}