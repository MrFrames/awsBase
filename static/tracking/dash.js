
$(".tabs").on("click", "li", function(){
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

var post_names = Object.keys(posts);
var option_list = [];
for (i=0; i<post_names.length; i++){
    name = post_names[i];
    option_list.push(document.createElement("option"));
    option_list[option_list.length-1].value = name;
    option_list[option_list.length-1].innerHTML = name;
    document.getElementById("post names").appendChild(option_list[option_list.length-1]);
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