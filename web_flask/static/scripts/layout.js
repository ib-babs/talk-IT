$(document).ready(() => {
  const collapseBtn = $("#collapse-btn"),
    navLink = $("nav");
  function theme(property) {
    if (property == "dark") {
      $(document.body).attr("style", "background:#222; color: white");
      $("textarea,#question_title,#edit-post-title").attr(
        "style",
        "background:#222; color: white"
      );
      $("#post-title").attr("style", "background:#222;");
      $('.user-username').css('color', '#eee')
      $("header").css("box-shadow", "0 3px 10px 0.3px #000");
      $("footer").css("box-shadow", "0 3px 10px 0.3px #000");
      $(".user-comments").attr(
        "style",
        "background: rgb(55, 55, 55);"
      );
      $(".question-body").css("box-shadow", "0 3px 10px 0.3px #000");
      $(".container").attr(
        "style",
        "background-color:#222; box-shadow: 0 1px 8px 0.5px #000"
      );
    } else {
      $("#question_title").attr("style", "background:initial;");
      $(document.body).attr("style", "background:initial; color: initial");
      $('.user-username').css('color', 'initial')
      $(".container").attr(
        "style",
        "background-color:#fff; box-shadow: 0 1px 8px 0.5px #ccc"
      );
      $(".question-body").css("box-shadow", "0 3px 10px 0.3px #ccc");
      $("header").css("box-shadow", "unset");
      $("footer").css("box-shadow", "unset");
      $(".user-comments").attr(
        "style",
        "background:rgba(210, 210, 210, 0.5)"
      );
      $("#post-title").attr("style", "background:white");
      $("textarea").attr("style", "background:white; color: initial");
    }
  }

  // Responsiveness
  collapseBtn.on("click", () => {
    if ($("nav").css("display") == "none")
      $("nav, #close-nav-on-blur").css("display", "grid");
    else $("nav, #close-nav-on-blur").css("display", "none");
  });
  $("#close-nav-on-blur").click(() => {
    $("nav, #close-nav-on-blur").css("display", "none");
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

  function parsingStyles(text, regex, symbol) {
    let style = text
      .split(regex)
      .filter(
        (part) =>
          part != undefined &&
          part.startsWith(symbol) &&
          part.endsWith(symbol) &&
          part[part.length - 2] != " " &&
          part != symbol
      );
    console.log(style);
    return style;
  }
  $.each($(".post-write-up"), function (idx, el) {
    let p = $(el).text().trimStart().trimEnd(),
      splitter = parsingStyles(
        p,
        /(?<=\*) +|(?!\*)\n|(\*(?=\S+)[^*]+\*)/gm,
        "*"
      ),
      italic = parsingStyles(p, /(?<=_) +|(?!_)\n|(_(?=\S+)[^_]+_)/gm, "_"),
      code = parsingStyles(p, /(?<=`) +|(?!`)\n|(`(?=\S+)[^`]+`)/gm, "`");
    p = p.replace(/</gim, "&lt;").replace(/>/gim, "&gt;");
    for (let index = 0; index < splitter.length; index++)
      p = p.replace(
        splitter[index],
        `<strong style="color: unset">${splitter[index].replace(
          /\*/gm,
          ""
        )}</strong>`
      );

    for (let index = 0; index < italic.length; index++)
      p = p.replace(italic[index], `<i>${italic[index].replace(/_/g, "")}</i>`);

    for (let index = 0; index < code.length; index++)
      p = p.replace(
        code[index],
        `<code style='background: #ddd; color: black;'>${code[index].replace(
          /`/g,
          ""
        )}</code>`
      );

    $(el).html(p);
  });
});
