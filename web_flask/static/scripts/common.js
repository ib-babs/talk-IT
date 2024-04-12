export function showHiddenPassword(elementID, passwordID) {
  $(elementID).click(() => {
    let password = $(passwordID);
    let passwordAttr = password.attr("type");
    if (passwordAttr === "password") {
      password.attr("type", "text");
      $(elementID).removeClass("fa-eye-slash").addClass("fa-eye");
    }
    if (passwordAttr === "text") {
      password.attr("type", "password");
      $(elementID).removeClass("fa-eye").addClass("fa-eye-slash");
    }
  });
}

export function fadeElement(elementID) {
  $(document).ready(() => {
    setTimeout(() => {
      $(elementID).fadeOut();
    }, 3000);
  });
}

export function shortenPostImages() {
  let imgsDiv = $(".post-body div.post-imgs-div");
  $.each(imgsDiv, function (indexInArray, imgDiv) {
    let child = imgDiv.children,
      imageRemainder = 0;
    for (let index = 0; index < child.length; index++) {
      if (index >= 3) {
        imageRemainder++;
        $(child[index]).css("display", "none");
      }
    }

    if (imageRemainder > 0) {
      $(imgDiv).append(`<div class='image-remain'><h2>+${imageRemainder} More</h2></div>`);
    }
  });
}
