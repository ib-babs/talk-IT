$(document).ready(() => {
  const collapseBtn = $("#collapse-btn"),
    navLink = $("nav");
  function theme(property) {
    if (property == "dark") {
      $(document.body).attr("style", "background:#222; color: white");
      $("textarea").attr("style", "background:#222; color: white");
      $("#question_title").attr("style", "background:#222; color: white");
      $("#edit-post-title").attr("style", "background:#222; color: white");
      $("#post-title").attr("style", "background:#222;");
      $("header").css("box-shadow", "0 3px 10px 0.3px #000");
      $("footer").css("box-shadow", "0 3px 10px 0.3px #000");
      $("#user-comments").attr(
        "style",
        "background:#222; box-shadow:0 3px 10px 0.3px #000"
        );
        $(".question-body").css("box-shadow", "0 3px 10px 0.3px #000");
        $(".container").attr(
          "style",
          "background-color:#222; box-shadow: 0 1px 8px 0.5px #000"
          );
        } else {
          $("#question_title").attr("style", "background:initial;");
          $(".container").css("box-shadow", "0 1px 8px 0.5px #f00");
          $(document.body).attr("style", "background:initial; color: initial");
          $(".container").attr(
            "style",
            "background-color:unset; box-shadow: 0 1px 8px 0.5px #ccc"
            );
            $(".question-body").css("box-shadow", "0 3px 10px 0.3px #ccc");
            $("header").css("box-shadow", "unset");
            $("footer").css("box-shadow", "unset");
      $("#user-comments").attr(
        "style",
        "background:rgba(210, 210, 210, 0.5); box-shadow:unset"
      );
      $("#post-title").attr("style", "background:white");
      $("textarea").attr("style", "background:white; color: initial");
    }
  }

  // Responsiveness
  collapseBtn.on("click", () => {
    if ($(navLink).css("display") == "none") $(navLink).css("display", "grid");
    else $(navLink).css("display", "none");
  });
  window.onresize = () => {
    if (window.innerWidth >= 768) $(navLink).css("display", "grid");
    else $(navLink).css("display", "none");
  };

  // Persistent theme
  if (localStorage.getItem("theme"))
    if (localStorage.getItem("theme") == "dark") {
      theme("dark");
    } else {
      theme("light");
    }

  $("#theme-label").click(() => {
    if (
      localStorage.getItem("theme") == "light" ||
      !localStorage.getItem("theme")
    ) {
      theme("dark");
      localStorage.setItem("theme", "dark");
    } else {
      localStorage.setItem("theme", "light");
      theme("light");
    }
  });
});
