var CropImage = (function() {
	function MainCrop () {
		var mc = $('#cropper');
		mc.croppie({
			viewport: {
				width: 150,
				height: 150,
				type: 'circle'
			},
			boundary: {
				width: 312,
				height: 200
			}
		});

		function readFile(input) {
 			if (input.files && input.files[0]) {
	            var reader = new FileReader();

	            reader.onload = function (e) {
					$('.upload-demo').addClass('ready');
	            	mc.croppie('bind', {
	            		url: e.target.result
	            	}).then(function(){
	            		console.log('jQuery bind complete');
	            	});
	            };
	            reader.readAsDataURL(input.files[0]);
	        }
	        else {
		        alert("Sorry - you're browser doesn't support the FileReader API");
		    }
		}

		setTimeout(function() {
			mc.croppie('bind', {
				url: $('#cropper').attr('src'),
				zoom: document.getElementsByClassName('cr-slider')[0].getAttribute('min')
			});
			setTimeout(function() {
				$('#div_img_crop').hide();
			}, 50);
		}, 250);

		mc.on('update.croppie', function (ev, data) {
			// console.log('jquery update', ev, data);
		});

		$('#save_img').on('click', function (ev) {
            mc.croppie('result', {
				type: 'rawcanvas',
				circle: true
            }).then(function (canvas) {
				var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            	$.ajax({url: "/save_photo_user/" + $('#user_id').val() + "/",
						data: { image : canvas.toDataURL() },
						type: 'POST',
						headers: {
							"X-CSRFToken": csrftoken
						},
						fail: function() {},
						success: function(res) {
							if(res.result == 'true') {
								$('#div_img_crop').show();
								setTimeout(function() {
									mc.croppie('bind', {
										url: '/media/' + res.image_big,
										zoom: document.getElementsByClassName('cr-slider')[0].getAttribute('min')
									});
									setTimeout(function() {
										$('#div_img_crop').hide();
									}, 50);
								}, 250);
							}
							else {
								console.log(res);
							}
						}
				});
			});
		});

		$('#upload_img').on('click', function (ev) {
            $('#upload_img_file').click();
		});

		$('#delete_img').on('click', function (ev) {
			var csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
			$.ajax({url: "/delete_photo_user/" + $('#user_id').val() + "/",
					type: 'POST',
					headers: {
						"X-CSRFToken": csrftoken
					},
					fail: function() {},
					success: function(res) {
						if(res.result == 'true') {
							$('#div_img_crop').show();
							setTimeout(function() {
								mc.croppie('bind', {
									url: '/media/' + res.image_big,
									zoom: 1.0336
								});
								setTimeout(function() {
									$('#div_img_crop').hide();
								}, 50);
							}, 250);
						}
						else {
							console.log(res);
						}
					}
			});
		});

		if($('input[name=image]').length==1) {
			$('input[name=image]').on('change', function () {
				if($(this).val() != '') {
					readFile(this);
				}
			});
		}
	}
	function init() {
		MainCrop();
	}
	return {
		init: init
	};
})();
