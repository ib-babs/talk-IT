$(document).ready(() => {
  let activeNav = $("nav .nav-link li");
  $(activeNav[1]).css("background", "blue");
  $(activeNav[1]).css("color", "white");

  $("#delete-question-btn").on("click", () => {
    let deleteModalContainer = $("#modal-container"),
      decisionButtons = $("#modal-container button");

    deleteModalContainer.css("display", "grid");
    $(decisionButtons[1]).click(() => {
      deleteModalContainer.css("display", "none");
    });
  });
});
