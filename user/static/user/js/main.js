function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$(document).ready(function () {

  $('characterWindow').click(function() {
    $('characterWindow').toggleClass('scale');
  })

  $(".characterWindow").click(function () {
    // console.log($(this).attr("value"));
    // console.log(getCookie("csrftoken"));

    $.ajax({
      type: "GET",
      url: "api/",
      headers: {
        csrfmiddlewaretoken: getCookie("csrftoken"),
      },

      data: {
        character_name: $(this).attr("value"),
      },

      success: function (response) {
        var character_items = response["character_items"];

        $("#equippedItemsContainer").empty();

        character_items.forEach((item) => {

          var flask = "";
          if (item.flask != "") {
            flask = item.flask;
          }

          var placement = "";
          if (item.type == "Weapon" || item.type == "Offhand") {
            if (item.height == 3) {
              placement = "placement";
            } 
            else if (item.height == 2) {
              placement = "placement2";
            }
          }

          fracturedMods= "";
          if(item.fracturedMods){
            item.fracturedMods.forEach((fractured) => {
              fracturedMods += '<p class="fracturedMod textMod">' + fractured + '</p>';
            });
          }

          implicitMods = "";
          if(item.implicitMods){
            item.implicitMods.forEach((implicit) => {
              implicitMods += '<p class="affixMod textMod">' + implicit + '</p>';
            }); 
          }

          explicitMods = "";
          if(item.explicitMods){
            item.explicitMods.forEach((explicit) => {
              explicitMods += '<p class="affixMod textMod">' + explicit + '</p>';
            }); 
          }

          craftedMods = "";
          if(item.craftedMods){
            item.craftedMods.forEach((crafted) => {
              craftedMods += '<p class="craftedMod textMod">' + crafted + '</p>';
            }); 
          }

          corrupted = "";
          if(item.corrupted){
            corrupted = '<p class="corrupted textMod">Corrupted</p>';
          }

          $('#equippedItemsContainer').append($("<div/>", {class: "itemContainer " + item.type + flask + " tooltip"})
                                        .append($("<div/>", { class: "iconContainer " + placement })
                                          .append($("<div/>", { class: "icon" })
                                            .append($("<img>", { src: item.icon }))))
                                            
                                        .append($("<span/>", { class: "tooltipText" }) // Tooltip span
                                          .append($("<div/>", {class:"itemName regionColor" + item.rarity + " md",}) 
                                            .append($("<p/>", {class:"rarity" + item.rarity + " m-0", text: item.name})) 
                                            .append($("<p/>", { class:"rarity" + item.rarity + " m-0", text: item.typeLine})))
                                          .append($("<div/>", {class: "itemMod"})
                                            .append($("<p/>", {class: "enchantMod textMod", text: item.enchantMods}))
                                            .append(fracturedMods)
                                            .append(implicitMods)
                                            .append(explicitMods)
                                            .append(craftedMods)
                                            .append(corrupted))) 
                                            )
                                      
                                      
        });

        // Tu pol naprej updejtaš html ...
      },

      error: function (response) {
        // alert the error if any error occured
      },
    });
  });
});
{
  /* <div class="itemContainer {{ item.type }}{% if item.flask %}{{item.flask}}{% endif %} tooltip"></div> */
}
