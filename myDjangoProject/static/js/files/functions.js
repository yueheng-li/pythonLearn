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
		var env = $("#env").val();
		if (!confirmM(env, "本番環境用warファイル作成を行います。よろしいでしょうか？")) {
			return;
		}
		$("body").mLoading({
		    text:"runing",//加载文字，默认值：加载中...
		}).show();
		$.get("/run?env=" + env, function(ret){
            $('#showlog').html(ret)
            $.get("/war?env=" + env, function(dict){
            	var tag = loadDate(dict);
				$('#uploader_filelist').html(tag);
            	console.log(dict);
            });
            $("body").mLoading("hide");
        })
	});


	// move
	$("#move").click(function(){
		var env = $("#env").val();
		if (!confirmM(env, "本番環境にwarをリリースします。よろしいでしょうか？")) {
			return;
		}
		$("body").mLoading({
		    text:"moving and tomcat restarting",//加载文字，默认值：加载中...
		}).show();
		$.get("/mv", function(ret){
            $('#showlog').html(ret)
            $.get("/rwar?env=" + env, function(dict){
            	var tag = '';
            	for (var i = 0; i < dict.length; i++) {
            		tag += loadDate(dict[i]);
            	}
				$('#uploader_filelist').html(tag);
            	
            	console.log(dict);
            });
            $("body").mLoading("hide");
        })
	});

	// stop
	$("#stop").click(function(){
		var env = $("#env").val();
		$("body").mLoading({
		    text:"stoping",//加载文字，默认值：加载中...
		}).show();
		$.get("/stop?env=" + env, function(ret){
            $('#showlog').html(ret)
            $("body").mLoading("hide");
        })
	});

	// start
	$("#start").click(function(){
		var env = $("#env").val();
		$("body").mLoading({
		    text:"starting",//加载文字，默认值：加载中...
		}).show();
		$.get("/start?env=" + env, function(ret){
            $('#showlog').html(ret)
            $("body").mLoading("hide");
        })
	});

	// pstree
	$("#ps").click(function(){
		var env = $("#env").val();
		$("body").mLoading({
		    text:"loading",//加载文字，默认值：加载中...
		}).show();
		$.get("/ps?env=" + env, function(ret){
            $('#showlog').html(ret)
            $("body").mLoading("hide");
        })
	});

	// view log
	$("#log").click(function(){
		var env = $("#env").val();
		$("body").mLoading({
		    text:"reviewing",//加载文字，默认值：加载中...
		}).show();
		$.get("/log?env=" + env, function(ret){
            $('#showlog').html(ret)
            $("body").mLoading("hide");
        })
	});

	// recovery
	$("#recovery").click(function(){
		var env = $("#env").val();
		if (!confirmM(env, "本番環境にwarを回復します。よろしいでしょうか？")) {
			return;
		}
		$("body").mLoading({
		    text:"recovering and tomcat restarting",//加载文字，默认值：加载中...
		}).show();
		$.get("/recovery?env=" + env, function(ret){
            $('#showlog').html(ret)
            $("body").mLoading("hide");
        })
	});

});

function loadDate(data) {
	if (data == null || data.path == null) {
		return "";
	}

	var tag = '<li id="p1bkoc3vom1rikach16gkkp6e9b4" class="plupload_delete">';
	if (data && data.path) {

		tag += ' <div class="plupload_file_name"><span>'+data.path+'</span></div>';
	} else {

		tag += ' <div class="plupload_file_name"><span></span></div>';
	}
	tag += ' <div class="plupload_file_action">';
	tag += ' <a href="#" style="display: block;"></a>';
	tag += ' </div>';
	if (data && data.ct) {

		tag += ' <div class="plupload_file_status">'+data.ct+'</div>';
	} else {

		tag += ' <div class="plupload_file_status"></div>';
	}
	
	tag += ' <div class="plupload_file_size"></div>';
	tag += ' <div class="plupload_clearer">&nbsp;</div>';
	tag += ' </li>';
	return tag;
}

function confirmM(env, message) {
	if (env != 'prod') {
		return true;
	}
	var r=confirm(message)
	if (r == true) {
		return true;
	}
	return false;
}