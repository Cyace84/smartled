jQuery.fn.toggleAttr = function(attr) {
 return this.each(function() {
  var $this = $(this);
  $this.attr(attr) ? $this.removeAttr(attr) : $this.attr(attr, attr);
 });
};

var requestUrl = `http://192.168.0.102/`;
function chagneColor(rgbColor) {
  let ledStrips = $('[led-on][led-selected]');
  
  let data = {
    "color": rgbColor,
    "strips": []
  };
  $.each(ledStrips, function (id, obj) {
    data.strips.push(obj.id)
  });
  

  // $.post(`http://192.168.0.107/`, data, function (data) { });
  if (data["strips"].length > 0) {
    $.post(requestUrl, data, function (data) { });
  }
}

function ledOff(strip) {
  let data = {
    "color": "rgb(0,0,0)",
    "strips": [strip]
  };
  $.post(requestUrl, data, function (data) { });
}

function ledOn(strip) {
  let data = {
    "color": colorPicker.color.rgbString,
    "strips": [strip]
  };
  $.post(requestUrl, data, function (data) { });
}

var colorPicker = new iro.ColorPicker(".colorPicker", {
  // color picker options
  // Option guide: https://iro.js.org/guide.html#color-picker-options
  width: 280,
  color: "rgb(255, 255, 0)",
  borderWidth: 1,
  borderColor: "#fff",
});

var values = document.getElementById("values");
var hexInput = document.getElementById("hexInput");

colorPicker.on(["color:init", "color:change"], function(color){
  values.innerHTML = [
    "hex: " + color.hexString,
    "rgb: " + color.rgbString,
    "hsl: " + color.hslString,
    ].join("<br>");
  
  
  chagneColor(color.rgbString)
  $("[led-on][led-selected]").css("color", color.hexString)
  // hexInput.value = color.hexString;
  // var q = $.get(`http://192.168.1.101/a/`, function (data) { })
  
});

hexInput.addEventListener('change', function() {
  colorPicker.color.hexString = this.value;
});



$('[led-tile]').on('click', function (e) {
  if (e.originalEvent.toElement.tagName === "use" ||
    e.originalEvent.toElement.tagName === "svg") {
    return false;
  }
  if (!e.target.hasAttribute("led-on")) {
    return false;
  }
  e.target.toggleAttribute("led-selected")

});
  
$('[led-tile]').on('dblclick', function (e) {
  if (e.originalEvent.toElement.tagName === "use" ||
    e.originalEvent.toElement.tagName === "svg") {
    return false;
  };
  let iconLed = e.currentTarget.children[1];
  
  iconLed.classList.toggle("is-hidden");
  
  e.target.style.color = '';
  e.target.toggleAttribute("led-on");

  if (e.target.hasAttribute("led-on")) {
    e.target.toggleAttribute("led-selected");
    e.target.style.color = colorPicker.color.hexString;
    ledOn(e.target.id);
  } else {
    if (e.target.hasAttribute("led-selected")) {
      e.target.toggleAttribute("led-selected");
    }
    ledOff(e.target.id);
  }
})

$('.zoom-in').on('click', function (e) {
  let target = e.currentTarget.parentElement
  target.classList.toggle("is-hidden");

  if (target.id === "cornersAll") {
    var ledChildList = $(".led-corner-list")[0].children
    $("#cornersCustom").toggleClass("is-hidden");

  } else if (target.id === "roofAll") {
    var ledChildList = $(".led-roof-list")[0].children
    $("#roofCustom").toggleClass("is-hidden");
  };

  $.each(ledChildList, function (id, obj) {
    if (id === 0) {
      return;
    };

    if (target.hasAttribute("led-on")) {
      obj.toggleAttribute("led-on");
      obj.toggleAttribute("led-selected");
      obj.children[1].classList.toggle("is-hidden");
      obj.style.color = colorPicker.color.hexString;
    }
  });
  if (target.hasAttribute("led-on")) {
    target.toggleAttribute("led-on");
    target.children[1].classList.toggle("is-hidden");
  };

});


$('.zoom-out').on('click', function (e) {
  
  let target = e.currentTarget.parentElement
  if (target.classList[0] === "led-corner-list") {
    var lastTarget = $("#cornersCustom");
    var newTarget = $("#cornersAll");

    var ledChildList = $(".led-corner-list")[0].children
    
  } else if (target.classList[0] === "led-roof-list") {
    var lastTarget = $("#roofCustom");
    var newTarget = $("#roofAll");

    var ledChildList = $(".led-roof-list")[0].children
  };
  lastTarget.toggleClass("is-hidden");
  newTarget.toggleClass("is-hidden");

  let chck = false;

  $.each(ledChildList, function (id, obj) {
    if (id === 0) {
      return;
    };

    if (obj.hasAttribute("led-on")) {
      chck = true;
      obj.toggleAttribute("led-on");
      obj.children[1].classList.toggle("is-hidden")
    } else {
      obj.style.color = "#fff";
    }
    
    if (obj.hasAttribute("led-selected")) {
      obj.toggleAttribute("led-selected")
    }
  });

  if (chck) {
    newTarget.toggleAttr("led-on");
    newTarget[0].children[1].classList.toggle("is-hidden");
    e.target.style.color = colorPicker.color.hexString;
  }
})

$('[fireflicker-tile]').on('click', function (e) {
  console.log(e.target)
  e.target.toggleAttribute("dynamic-active");
  $(".modes").toggleAttr("dynamic-selected");
  $(".dynamic").toggleAttr("dynamic-selected")
  $(".fireflicker-form").toggleClass("is-hidden")

});
$('[rainbow-tile]').on('click', function (e) {
  console.log(e.target)
  e.target.toggleAttribute("dynamic-active");
  $(".modes").toggleAttr("dynamic-selected");
  $(".dynamic").toggleAttr("dynamic-selected")
  $(".rainbow-form").toggleClass("is-hidden")

});


$('[mode-nav]').on('click', function (e) {
  let = prevMode = document.querySelector("[active-mode]");
  if (prevMode === null) {
  } else {
      if (prevMode.id === e.target.id) {
      } else {
        let i = $("[active-mode]")
        $(".colorpicker").toggleClass("is-hidden")
        $(".dynamic").toggleClass("is-hidden")
        prevMode.toggleAttribute("active-mode");
        $("[active-mode]")
      }
  };

  e.target.toggleAttribute("active-mode")

})


$('.submit-btn').on('click', function (e) {
  let modeName = e.target.parentElement.classList[1].slice(0, -5);
  if (modeName === "fireflicker") {
    var formElement = document.querySelector(".fireflicker-form");
  } else {
    var formElement = document.querySelector(".rainbow-form");
  }
  
  let form = new FormData(formElement);
  let br = 0;
  let speed = 0;
  for (var pair of form.entries()) {
    
    if (pair[0] === "brightness") {
      br = pair[1];
    } else if (pair[0] === "speed") {
      speed = pair[1];
    }
  };

  let color = $(".checkbox:checked")[0].id;
  
  let ledStrips = $('[led-on]:not([led-selected])');
  let strips = []
  
  $.each(ledStrips, function (id, obj) {
    strips.push(obj.id)
  });
  
  let data = {
    "dynamic": modeName,
    "colorDynamic": color,
    "brightness": br,
    "speed": speed,
    "strips": strips
  };
  console.log(modeName)
  if (data["strips"].length > 0) {
    $.post(requestUrl, data, function (data) { });
  }
})

