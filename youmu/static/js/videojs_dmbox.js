videojs.plugin('DMB', DMBox);
function DMBox() {
	var player = this.el().children[0]

	box = document.createElement('div');
	box.className = "vjs-dmbox";
	box.style.display = "none";
	this.el().insertBefore(box, this.el().getElementsByClassName("vjs-error-display")[0]);

	var boxControl = document.createElement("div");
	boxControl.className = "vjs-dmbox-control vjs-menu-button vjs-control";
	boxControlContent = document.createElement("span");
	boxControlContent.className = "fi-quote";
	boxControl.appendChild(boxControlContent);
	this.el().getElementsByClassName("vjs-control-bar")[0].appendChild(boxControl);

	boxControl.onclick = function() {
		box = document.getElementsByClassName("vjs-dmbox")[0];
		if (box.style.display == "none") {
			box.style.display = "block";
			box.innerHTML = "<span class='vjs-closeDMBox fi-x' onclick='var box = document.getElementsByClassName(\"vjs-dmbox\")[0];box.style.display = \"none\";'></span>";
			dmContent = document.createElement("input");
			dmContent.id = "vjs-dmbox-content";
			dmContent.type = "text";
			dmContent.placeholder = "弹幕内容";
			dmContent.addEventListener("keydown", function(e) {
				var theEvent = e || window.event;  
				var code = theEvent.keyCode || theEvent.which || theEvent.charCode;
				if (code == 13) {
					var currentTime = player.currentTime;
					content = document.getElementById("vjs-dmbox-content").value;
					fontsize = [12, 16, 18, 25, 36, 45, 64];
					pools = [0, 1];
					modes = [1, 4, 5, 6];
					$.ajax({
						"type": "post", 
						"url": "/api/barrage/video/" + $("#video_id").val(), 
						"contentType": "application/json", 
						"data": JSON.stringify({
							"position": currentTime,
							"mode": modes[parseInt(Math.random() * modes.length)],
							"size": fontsize[parseInt(Math.random() * fontsize.length)],
							"color": parseInt(Math.random() * 16777215),
							"pool": pools[parseInt(Math.random() * pools.length)],
							"content": content
						}),
						"dataType": "json", 
						"success": 
							function(data) {
								//alertInfo(JSON.stringify("发送成功", 300));
								box = document.getElementsByClassName("vjs-dmbox")[0];
								box.style.display = "none";
							}
					});
				}
			});
		} else {
			box.style.display = "none";
		}
		box.appendChild(dmContent);
	};
}
