import { showHiddenPassword, fadeElement } from "./common.js";
showHiddenPassword("#pwd-show", "INPUT#password");
showHiddenPassword("#c-pwd-shown", "INPUT#confirm_password");

fadeElement('#flash-message')