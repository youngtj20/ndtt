		function preview_snapshot() {
			// freeze camera so user can preview pic
			Webcam.freeze();
			document.getElementById('pre_take_buttons').style.display = 'none';
			document.getElementById('post_take_buttons').style.display = '';
		}
		
		function cancel_preview() {
			// cancel preview freeze and return to live camera feed
			Webcam.unfreeze();
			// swap buttons back
			document.getElementById('pre_take_buttons').style.display = '';
			document.getElementById('post_take_buttons').style.display = 'none';
		}
		
		function save_photo() {
			// actually snap photo (from preview freeze) and display it
			Webcam.snap( function(data_uri) {
			    var raw_image_data = data_uri.replace(/^data\:image\/\w+\;base64\,/, '');
			    document.getElementById('myphotodata').value = raw_image_data;
			    document.getElementById('myuploadcapture').submit();
			} );
		}

		function start_video_for_video(){
			Webcam.set({
	            width: 240,
	            height: 240,
	            image_format: 'jpeg',
	            jpeg_quality: 90
          	});
          	Webcam.attach( '#video' );
		}

		function start_video_for_still(){
			Webcam.set({
	            width: 240,
	            height: 240,
	            image_format: 'jpeg',
	            jpeg_quality: 90
          	});
          	Webcam.attach( '#camera' );
		}