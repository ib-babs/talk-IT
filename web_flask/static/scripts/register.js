import { showHiddenPassword, fadeElement } from "./common.js";
showHiddenPassword("#pwd-show", "INPUT#password");
showHiddenPassword("#c-pwd-shown", "INPUT#confirm_password");

$("#register-form").submit((e) => {
  let password = $("INPUT#password");
  let cpassword = $("INPUT#confirm_password");
  if (password.val() != cpassword.val()) {
    $("p#incorrect-pwd").text("Password does not match!");
    e.preventDefault();
  } else {
    $("#account-success").css("display", "grid");
  }
});

fadeElement('#flash-message')