import { showHiddenPassword, fadeElement } from "./common.js";
showHiddenPassword("#pwd-show", "INPUT#password");
$("#login-form").submit((e) => {
  $("#account-success").css("display", "grid");
});
fadeElement("#flash-message");
