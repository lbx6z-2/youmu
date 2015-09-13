angular.module('youmuApp', ['mm.foundation'])
	.service('UserService', function() {
		var id = "", name = "", avatar = "", admin = false;
		return {
			getID: function() {
				return id;
			},
			getName: function() {
				return name;
			},
			getAvatar: function() {
				return avatar;
			},
			isAdmin: function() {
				return admin;
			},
			setUser: function(_id, _name, _avatar, _admin) {
				id = _id;
				name = _name;
				avatar = _avatar;
				admin = _admin;
			},
			isLogin: function() {
				return id.length > 0;
			},
			logout: function() {
				id = "";
				name = "";
			}
		};
	});

var alertInfo = function(info, vanishTime) {
	vanishTime = vanishTime ? vanishTime : 3000;
	$("#alertInfo").html(info);
	$("#alertModal").foundation("reveal", "open");
	setTimeout(function() {
		$("#alertModal").foundation("reveal", "close");
	}, vanishTime);
};

var topBarCtrl = function ($scope, $rootScope, $http, UserService) {
	$scope.logoUrl = "/static/img/youmu-seal.jpg";
	$scope.isLogin = false;
    searchId = "";
    keyword = "";
    $scope.search = function() {
        window.location.href = "/?query=" + $("#query").val();
    };
	$('#searchForm').on('valid.fndtn.abide', function() {
		$scope.search();
	});
	$scope.checkLogin = function() {
		$http.get("/api/user/_me").success(
			function(data, status){
				if (data.hasOwnProperty("id")) {
					UserService.setUser(data.id, data.name, data.avatar, data.admin);
					$scope.user_id = UserService.getID();
					$scope.username = UserService.getName();
					$scope.avatar = UserService.getAvatar();
					$scope.isAdmin = UserService.isAdmin();
					$scope.logout = function() {
						$http.post("/api/user/_logout").success(		
							function(data, status) {
								UserService.logout();
								$scope.checkLogin();
							}
						).error(
							function(data, status) {
								alertInfo("登出失败");
							}
						);	
					};
					$rootScope.$emit('logined');
				} else {
					$('#loginForm').on('valid.fndtn.abide', function() {
						$("#loginButton").attr("disabled", "disabled");
						var user_id = $("#user_id").val();
						var password = $("#password").val();
						$http.post("/api/user/_login", 
							{
								"username": user_id,
								"password": password
							}).success(
								function(data, status) {
									$("#loginButton").removeAttr("disabled");
									if (data.state === "ok") {
										$('#loginModal').foundation('reveal', 'close');
										$scope.checkLogin();
									} else {
										$("#loginFormFieldset").append(
											'<div data-alert class="alert-box alert radius">'+
												'用户名或密码错误'+
												'<a href="#" class="close">&times;</a>'+
											'</div>'
										).foundation();
									}
								}
							).error(
								function(data, status) {
									$("#loginButton").removeAttr("disabled");
									$("#loginFormFieldset").append(
										'<div data-alert class="alert-box warning radius">'+
											'服务器繁忙，请稍候再试'+
											'<a href="#" class="close">&times;</a>'+
										'</div>'
									).foundation();
								}
							);
					});
				}
				$scope.isLogin = UserService.isLogin();
			}
		).error(
			function(data, status){
				alertInfo("获取用户信息出错");
			}
		);
	};
	$scope.checkLogin();
};

var videoStoreCtrl = function ($scope, $rootScope, $http) {
	$scope.logoUrl = "/static/img/youmu-circle.png";
	$scope.authorUrl = "/static/img/youmu-seal.jpg";
	var url = "/api/video/";
	if ($("#query_str").val() != "") 
		url = "/api/videolist/_search?keyword=" + $("#query_str").val();
	$http.get(url).success(function(data, status) {
		$rootScope.videos = [];
		for (var i = 0; i < data.length; ++i) {
			item = data[i];
			item.videoUrl = "/videos/" + item.video_id;
			if (item.title.search(keyword) != -1 ||
				item.owner_id.search(keyword) != -1 ||
				item.description.search(keyword) != -1 ||
				item.category.search(keyword) != -1
			   )
			{
				$rootScope.videos.push(item);
			}
		}
	});
};

var videoDataCtrl = function ($scope, $rootScope, $http, UserService) {
	$http.get("/api/video/" + $("#video_id").val()).success(function(data, status) {
		$scope.video = data;
		var url, mtype;
		if (data.media_type != "live") {
			mtype = "video/mp4";
			url = "http://" + document.domain + ":8888/" + data.video_id;
		} else {
			mtype = "rtmp/mp4";
			if (data.url == "") {
				url = "rtmp://" + document.domain + ":1935/myapp/" + data.video_id;
			} else {
				url = data.url;
			}
		}
		$(".video-player-container").append(
			'<video id="playbox" class="video-js vjs-default-skin" controls preload="auto" poster="'+data.cover+'" data-setup="{}" width="100%">'+
				'<source src="'+url+'" id="playboxUrl" type="'+mtype+'" />'+
				'<p class="vjs-no-js">'+
					'To view this video please enable JavaScript, and consider upgrading to a web browser'+
					'that <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>'+
				'</p>'+
			'</video>'
		);
		window.thevideojs = videojs("playbox");
		if (data.media_type != "live") {
			thevideojs.ABP();
			thevideojs.danmu.load("/api/barrage/video/" + data.video_id);
			thevideojs.DMB();
		}
	});
	$http.get("/api/comment/video/" + $("#video_id").val()).success(function(data, status) {
		$scope.video.comments = data;
		$scope.video.comments_count = data.length;
	});
	$http.post("/api/video/" + $("#video_id").val() + "/_play").success(function(data, status) {});
	$scope.refreshCommentBox = function() {
		$http.get("/api/comment/video/" + $("#video_id").val()).success(
			function(data, status) {
				$scope.comments = data;
			}
		).error(
			function(data, status) {
				alertInfo("获取评论失败");
			}
		);
	};
	$scope.refreshCommentBox();
	$rootScope.$on('logined', function() {
		$scope.user_id = UserService.getID();
		$scope.isAdmin = UserService.isAdmin();
		$scope.refreshLike = function() {
			$http.get("/api/video/" + $("#video_id").val() + "/_like/_me").success(function(data, status) {
				$scope.melike = data.like == "yes";
			});
			$http.get("/api/video/" + $("#video_id").val() + "/_like").success(
				function(data, status) {
					$scope.video.like = data.total;
				}
			).error(
				function(data, status) {
					alertInfo(data + "<br>Code:" + status);
				}
			);
		};
		$scope.refreshLike();
		$scope.likeVideo = function() {
			$http.post("/api/video/" + $("#video_id").val() + "/_like").success(
				function(data, status) {
					$scope.refreshLike();
				}
			).error(
				function(data, status) {
					alertInfo(data + "<br>Code:" + status);
				}
			);
		};
		$('#commentForm').on('valid.fndtn.abide', function() {
			$("#commentButton").attr("disabled", "disabled");
			$http.post("/api/comment/video/" + $("#video_id").val(),
			{
				"content":$("#commentContent").val()
			}).success(
				function(data, status) {
					//$("#commentContent").blur();
					$("#commentContent").val("");
					$("#commentButton").removeAttr("disabled");
					$scope.refreshCommentBox();
				}
			).error(
				function(data, status) {
					alertInfo(data + "<br>Code:" + status);
					$("#commentButton").removeAttr("disabled");
				}
			);
		});
		$scope.delComment = function(comment_id) {
			$http.delete("/api/comment/" + comment_id).success(
				function(data, status) {
					alertInfo("评论删除成功");
					$scope.refreshCommentBox();
				}
			).error(
				function(data, status) {
					alertInfo(data + "<br>Code:" + status);
				}
			);
		};
	});
};

var personalCenterCtrl = function ($scope, $rootScope, $http, UserService) {
	$rootScope.$on('logined', function() {
		$scope.username = UserService.getName();
		$scope.user_id = UserService.getID();
		$scope.isAdmin = UserService.isAdmin();
		$scope.avatar = UserService.getAvatar();
		$scope.get_videos = function(){
			if (UserService.isAdmin()) url = "/api/video/"; else url = "/api/videolist/owner/" + $scope.user_id; 
			$http.get(url).success(
				function(data, status) {
					$scope.videos = [];
                    for (var i = 0; i < data.length; ++i) {
                        item = data[i];
                        item.videoUrl = "/videos/" + item.video_id;
                        $http.get("/api/comment/video/" + item.video_id).success(
                            function(data, status) {
                                item.comments = data;
                                item.commentsLen = data.length;
                            }
                        );
						$scope.videos.push(item);
					}
				}
				//"owner_name":"曼联第四","description":"如题","tags":[],"banned":false,"play_count":16,"owner_avatar":"/static/uploads/images/u1lkdXl_blueberry_chrome.jpg","disabled":false,"upload_time":"2014-11-11 01:48:20","like":1,"title":"膜拜badpoet","video_id":"8","cover":"/static/uploads/images/uxa5m3R_save_5000_214503_1e-8.jpg","length":0,"owner_id":"hwr12","videoUrl":"/videos/8"} 
			).error(
				function(data, status) {
					alertInfo("获取上传视频列表失败<br>Code:" + status);
				}
			);
		};
		$scope.get_videos();

        $scope.getCategory = function() {
            $http.get("/api/video/_categories").success(
                function(data, status) {
                    $scope.categories = [];
                    for (var i = 0; i < data.categories.length; ++ i)  {
                        item = data.categories[i];
                        $scope.categories.push(item);
                    }
                }
            );
        };      

		$scope.DisableVideo = function(id) {
			$http.post("/api/video/" + id + "/_disable").success(
				function(data, status) {
					$scope.get_videos();
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
				}
			);
		};
		$scope.EnableVideo = function(id) {
			$http.post("/api/video/" + id + "/_enable").success(
				function(data, status) {
					$scope.get_videos();
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
				}
			);
		};
		$scope.ToggleVideoEnableDisable = function(id) {
			$http.get("/api/video/" + id).success(
				function(data, status) {
                    $scope.get_videos();
                    if(data.disabled) {
                        $scope.EnableVideo(id);
                    }
                    else {
                        $scope.DisableVideo(id);
                    }
                    $scope.get_videos();
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
				}
			);
		};
		$scope.BanVideo = function(id) {
			$http.post("/api/video/" + id + "/_ban").success(
				function(data, status) {
					$scope.get_videos();
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
				}
			);
		};
		$scope.UnbanVideo = function(id) {
			$http.post("/api/video/" + id + "/_unban").success(
				function(data, status) {
					$scope.get_videos();
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
				}
			);
		};
		$scope.ToggleVideoBanUnban = function(id) {
			$http.get("/api/video/" + id).success(
				function(data, status) {
                    $scope.get_videos();
                    if(data.banned) {
                        $scope.UnbanVideo(id);
                    }
                    else {
                        $scope.BanVideo(id);
                    }
                    $scope.get_videos();
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
				}
			);
		};

		$scope.getUsers = function(){
			$http.get("/api/user").success(
				function(data, status) {
					$scope.users = data.result;
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
					$scope.users = [];
				}
			);
		};

		if ($scope.isAdmin){
			$scope.getUsers();
		}

		$scope.EnableUser = function(user_id){
			$http.post("/api/user/" + user_id + "/_enable").success(
				function(data, status) {
					alertInfo("解禁成功");
					$scope.getUsers();
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
				}
			);
		};

		$scope.DisableUser = function(user_id){
			$http.post("/api/user/" + user_id + "/_disable").success(
				function(data, status) {
					alertInfo("屏蔽成功");
					$scope.getUsers();
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
				}
			);
		};

        $scope.ToggleUserEnableDisable = function(user_id){
			$http.get("/api/user/" + user_id).success(
				function(data, status) {
                    if(data.disabled) {
                        $scope.EnableUser(user_id);
                    }
                    else {
                        $scope.DisableUser(user_id);
                    }
					$scope.getUsers();
				}
			).error(
				function(data, status) {
					alertInfo("服务器繁忙，稍后再试");
				}
			);
        };

        $scope.ToggleUserIsAdmin = function(user_id){
            $http.post("/api/user/" + user_id + "/_toggle-admin").success(
                function(data, status) {
                    $scope.getUsers();
                }
            ).error(
                function(data, status) {
                    alertInfo("服务器繁忙，稍后再试");
                }
            );
        };

		$('#modifyProfileForm').on('valid.fndtn.abide', function() {
			$("#modifyProfileButton").attr("disabled", "disabled");
			$("#modifyProfileForm").ajaxSubmit({
				type:'put',
				url: "/api/user/_me", 
				success: function(data) {
					location.reload();
					$("#modifyProfileButton").removeAttr("disabled");
                    data = JSON.parse(data);
                    console.log(data.state);
                    if(data.content === "name is taken") {
                        console.log("用户名已有人使用");
                    }
				},
				error: function(e) {
					$("#modifyProfileButton").removeAttr("disabled");
					alertInfo("上传失败"/* + e.responseText*/);
				}
			});
		});
		$('#uploadVideoForm').on('valid.fndtn.abide', function() {
			$("#uploadVideoButton").attr("disabled", "disabled");
			$("#uploadVideoForm").ajaxSubmit({
				type:'post',
				url: "/api/video/upload", 
				beforeSubmit: function() {
					alertInfo("开始上传");
				},
				uploadProgress: function(event, position, total, percentComplete) {
					alertInfo("上传进度: " + percentComplete + "%", 100000);
				},
				success: function(data) {
					res = JSON.parse(data);
					$("#uploadVideoButton").removeAttr("disabled");
					$scope.get_videos();
					alertInfo(res.state);
				},
				error: function(e) {
					$("#uploadVideoButton").removeAttr("disabled");
					alertInfo("上传失败"/* + e.responseText*/);
				}
			});
		});
	});
};
