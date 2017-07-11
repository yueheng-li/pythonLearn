$(function() {
	//===== Add classes for sub sidebar detection =====//
	if ($('div').hasClass('secNav')) {
		$('#sidebar').addClass('with');
		//$('#content').addClass('withSide');
	}
	else {
		$('#sidebar').addClass('without');
		$('#content').css('margin-left','100px');//.addClass('withoutSide');
		$('#footer > .wrapper').addClass('fullOne');
	};

	$("#runAntBuild").click(function(){
		$("body").mLoading({
		    text:"downloading",//加载文字，默认值：加载中...
		}).show();
		$.get("/run", function(ret){
            $('#showlog').html(ret)
            $.get("/war", function(dict){
            	loadDate(dict)
            	console.log(dict);
            });
            $("body").mLoading("hide");
        })
	});
});

function loadDate(data) {

	var tag = '<li id="p1bkoc3vom1rikach16gkkp6e9b4" class="plupload_delete">';
	if (data && data.path) {

		tag += ' <div class="plupload_file_name"><span>'+data.path+'</span></div>';
	} else {

		tag += ' <div class="plupload_file_name"><span>1-9.PNG</span></div>';
	}
	tag += ' <div class="plupload_file_action">';
	tag += ' <a href="#" style="display: block;"></a>';
	tag += ' </div>';
	if (data && data.ct) {

		tag += ' <div class="plupload_file_status">'+data.ct+'</div>';
	} else {

		tag += ' <div class="plupload_file_status">2017-07-11T15:14:17</div>';
	}
	
	tag += ' <div class="plupload_file_size"></div>';
	tag += ' <div class="plupload_clearer">&nbsp;</div>';
	tag += ' </li>';
	$('#uploader_filelist').html(tag);
}
