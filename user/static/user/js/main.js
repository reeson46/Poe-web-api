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

  $('.characterWindow').click(function () {

    $('.characterWindow').removeClass('selectedCharacter'); // Remove 'color' CSS Class from all windows
    
    $(this).addClass('selectedCharacter');

    $.ajax({
      type: 'GET',
      url: 'api/character_detail/',
      headers: {
        csrfmiddlewaretoken: getCookie('csrftoken'),
      },

      data: {
        character_name: $(this).attr('value'),
      },

      success: function (response) {
        var character_items = response['character_items'];

        $('#equippedItemsContainer').empty();
        $('#itemsToDisplay').empty();

        character_items.forEach((item) => {
          
          flask = "";
          if (item.flask != "") {
            flask = item.flask;
          }

          placement = "";
          if (item.inventoryId == "Weapon" || item.inventoryId == "Offhand") {
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

          utilityMods = '';
          if(item.utilityMods){
            item.utilityMods.forEach((utility) => {
              utilityMods += '<p class="affixMod textMod">' + utility + '</p>';    
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

          if(item.inventoryId != 'MainInventory'){

            $('#equippedItemsContainer').append($("<div/>", {class: "itemContainer " + item.inventoryId + flask + " tooltip"})
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
                                              .append(utilityMods)
                                              .append(implicitMods)
                                              .append(explicitMods)
                                              .append(craftedMods)
                                              .append(corrupted))) 
                                              )
          }else{         
            $('#itemsToDisplay').append($('<div/>', {class: 'inventoryItem tooltip', style: 'top: calc('+ item.y + ' * var(--inventoryItemPosY)); left: calc(' + item.x + ' * var(--inventoryItemPosX));'})
                                  .append($("<div/>", { class: "iconContainer " + placement })
                                    .append($('<div/>', {class : 'icon'})
                                      .append($('<img>', {src: item.icon}))))
                                  
                                  .append($("<span/>", { class: "tooltipText" }) // Tooltip span
                                  .append($("<div/>", {class:"itemName regionColor" + item.rarity + " md",}) 
                                    .append($("<p/>", {class:"rarity" + item.rarity + " m-0", text: item.name})) 
                                    .append($("<p/>", { class:"rarity" + item.rarity + " m-0", text: item.typeLine})))
                                  .append($("<div/>", {class: "itemMod"})
                                    .append($("<p/>", {class: "enchantMod textMod", text: item.enchantMods}))
                                    .append(fracturedMods)
                                    .append(utilityMods)
                                    .append(implicitMods)
                                    .append(explicitMods)
                                    .append(craftedMods)
                                    .append(corrupted))) 
                                    )
   
          }
         

                                      
                                      
        });

      },

      error: function (response) {
        // alert the error if any error occured
      },
    });
  }); 

  $('.stashbtn').click(function () {

    $('.stashbtn').removeClass('selectedTab'); // Remove 'filter' CSS Class from all windows
    
    $(this).addClass('selectedTab');
    
    $.ajax({
      type: 'GET',
      url: 'api/stashtab/',
      headers: {
        csrfmiddlewaretoken: getCookie('csrftoken'),
      },

      data: {
        stashtab_index: $(this).attr('value')
      },

      success: function (response){

        $('#stashContent').empty();

        var stash_items = response['stash_items'];
        
        stash_items.forEach((item) => {

          ninjaUrl_btn = ''
          if (item.ninjaUrl){
            ninjaUrl_btn= '<a href="' + item.ninjaUrl + '"><button class="poeNinjaBtn">Poe Ninja</button></a>';
          }

          $('#stashContent').append($('<div/>', {class: 'item'})
                              .append($('<div/>', {class: 'icon'})
                                .append($('<img>', {src: item.icon, alt: ''})))
                              .append($('<div/>', {class: 'name'})
                                .append($('<h2/>', {text: item.typeLine})))
                              .append($('<div/>', {class: 'pn-link'})
                                .append(ninjaUrl_btn))
                              .append($('<div/>', {class: 'quantity'})
                                .append($('<h2/>', {text: item.quantity})))
                                );
        });
      },

      error: function (response){

      },

    });
  });
});

