$(document).ready(function() {
	
	$('form').submit(function(event) {
		event.preventDefault();
		/*Insert Button Management Here*/
		var loadingtext = "<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true' text='loading'></span> Downloading Logs...Do Not Close the Window"
		
		/*$('#btn').html(loadingtext); /*Toggle between text and button method
		$('#btn').button('loading');*/
		$('#loadingModal').modal('show')
		$.ajax({
			data : JSON.stringify({
				mgmtipid : $('#mgmtip').val(),
				userid : $('#user').val(),
				passwordid : $('#passwd').val(),
				rsi: $('#downloads-0').is(':checked'),
				varlog:$('#downloads-1').is(':checked'),
				both:$('#downloads-2').is(':checked')
			}),
			type : 'POST',
			url : '/_getrsi',
			dataType : 'json',
			contentType: "application/json",

		})
		.done(function(data) {

			if (data.errormsg) {
				console.log(data.errormsg);
				$('#loadingModal').modal('hide')
				$("#btn").text('Collect Support Logs'); /*Toggle between text and button methods
				$('#btn').button('reset');*/
				$("#succmsg").hide();
				$("#errmsg").text(data.errormsg).show();

			}

			if (data.successmsg) {
				console.log(data.successmsg);
				$('#loadingModal').modal('hide')
				$("#btn").text('Collect Support Logs'); /*Toggle between text and button methods
				$('#btn').button('reset');*/
				$("#errmsg").hide();
				if (data.coredump == "True") {
				var updatetable = ""
				for ( var a=0; a<data.rpcreply.length; a++){
					updatetable += '<tr><td><input type="checkbox"></td><td>'+data.rpcreply[a].filename+'</td><td>'+data.rpcreply[a].time+'</td></tr>'
				}
				$('#filelist > tbody:last-child').append(updatetable);
				$('#coredumpModal').modal('show')
				
				}
				$("#succmsg").text(data.successmsg).show();
				$(location).attr('href', '_sendf/'.concat(data.filename))

				

			}

		});


	});

});

