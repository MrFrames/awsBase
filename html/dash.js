console.log("dash.js version 1.6")

$(".tabs").on("click", ".tab-btn", function(){
  var tabsId = $(this).attr("id");
  $(this).addClass("active").siblings().removeClass("active");
  $('#' + tabsId + '-content-box').addClass("active").siblings().removeClass("active");
  $('#' + tabsId + '-content-box').removeClass("hide").siblings().addClass("hide")
  if ($(this).attr("id") === "tab-three"){
      console.log("tag3")
      sectionMap.setZoom(4)
  };
});

document.getElementById("save_post").addEventListener("click",function(){
    document.getElementById("post_content").innerHTML = (quill.root.innerHTML); 
});

if (saved !== "0"){
    $('#tab-two-content-box').addClass("active").siblings().removeClass("active");
    $('#tab-two-content-box').removeClass("hide").siblings().addClass("hide")
};

function check(){
    var checkbox = document.getElementById('meetUp');
    if (!checkbox.checked){
        console.log("activated");
        document.getElementById("ptitle").innerHTML = "Post Title:";
        document.getElementById("title").innerHTML = "Save Post";
        $('#post_names').addClass("active").removeClass("hide");
        $('#post_title').addClass("active").removeClass("hide");
        $('#editor').addClass("active").removeClass("hide");
        $('#pic').addClass("active").removeClass("hide");
    } else {
        console.log("hidden");
        document.getElementById("title").innerHTML = "Save meet-up pin:";
        document.getElementById("ptitle").innerHTML = "";
        $('#post_names').addClass("hide").removeClass("active");
        $('#post_title').addClass("hide").removeClass("active");
        $('#editor').addClass("hide").removeClass("active");
        $('#pic').addClass("hide").removeClass("active");
        
    }
}

var checked = 0;
$('#meetUp').change(function(){
    if (checked===0){

        checked = 1;
    } else {

        checked = 0;
    }
});

var post_names = Object.keys(posts);
var option_list = [];
for (i=0; i<post_names.length; i++){
    name = post_names[i];
    option_list.push(document.createElement("option"));
    option_list[option_list.length-1].value = name;
    option_list[option_list.length-1].innerHTML = name;
    document.getElementById("post_names").appendChild(option_list[option_list.length-1]);
};

function auto_fill(){
    name = document.getElementById("post names").value;
    console.log("name from dropdown:");
    console.log(name);
    coord = posts[name]["coord"];
    
    document.getElementById('placePk').value = posts[name]["placePk"];
    document.getElementById('name').value = posts[name]["place_name"];
    document.getElementById('lat').value = coord["lat"];
    document.getElementById('lng').value = coord["lng"];

    document.getElementById('postPk').value = posts[name]["postPk"];
    document.getElementById('post_title').value = name;
    quill.root.innerHTML = posts[name]["content"];
}

var section_names = Object.keys(sections);
var secOption_list = [];
for (i=0; i<post_names.length; i++){
    name = section_names[i];
    secOption_list.push(document.createElement("option"));
    secOption_list[secOption_list.length-1].value = name;
    secOption_list[secOption_list.length-1].innerHTML = name;
    document.getElementById("section names").appendChild(secOption_list[secOption_list.length-1]);
};

function auto_fillSections(){
    if (directionsDisplay){
        directionsDisplay.setMap(null);
    }
    directionsService =  new google.maps.DirectionsService;
    name = document.getElementById("section names").value;
    waypoints = sections[name]["waypoints"];
    if (!waypoints){
        waypoints = [];
    }
    console.log("waypoints")
    console.log(waypoints)
    start = sections[name]["start"]
    end = sections[name]["end"]
    
    document.getElementById('section pk').value = sections[name]["secPk"];
    document.getElementById('section name').value = name;
    document.getElementById('start').value = start;
    document.getElementById('waypoints').value = waypoints;
    document.getElementById('end').value = end;
    var locations = [];
    var waypoint_keys = Object.keys(waypoints)
    for (i=0; i< waypoint_keys.length; i++){
        locations.push({location:waypoints[i]});
    }
    request = getDirectionRequest(start,end,locations,"BICYCLING");
    directionsService.route(request,directionResults);
    
    function directionResults(result, status){
        var directionsDisplay = new google.maps.DirectionsRenderer({
            draggable: true,
            map: sectionMap
        });
        directionsDisplay.setDirections(result);
        directionsDisplay.setMap(sectionMap);
    } 
}

function getDirectionRequest(start,end, waypoints, travelMode){
    x = {
        origin: start,
        destination: end,
        travelMode: travelMode,
        optimizeWaypoints: true,
    };
    if (waypoints){
        x["waypoints"] = waypoints
    }
    return x
}
