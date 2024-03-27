
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
