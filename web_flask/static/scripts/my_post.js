import { shortenPostImages } from "./common.js";
$(document).ready(() => {
  let activeNav = $("nav .nav-link li");
  $(activeNav[1]).css("background", "blue");
  $(activeNav[1]).css("color", "white");

  $.each($(".delete-question-btn"), function (indexInArray, deleteBtn) {
    $(deleteBtn).on("click", () => {
      let deleteModalContainer = $(".modal-container"),
        delNoBtn = $(".modal-container .del-no-btn");
      $(deleteModalContainer[indexInArray]).css("display", "grid");

      // // Modal container
      $(delNoBtn[indexInArray]).click(() => {
        $(deleteModalContainer[indexInArray]).css("display", "none");
      });

      // // ===End modal == //
    });
  });

  shortenPostImages()
});
