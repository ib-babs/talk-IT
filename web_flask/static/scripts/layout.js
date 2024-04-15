$(document).ready(() => {
  const collapseBtn = $("#collapse-btn"),
    navLink = $("nav");
  function theme(property) {
    if (property == "dark") {
      $(document.body).attr("style", "background:#111; color: white");
      $("textarea,#post_title,#edit-post-title").attr(
        "style",
        "background:#222; color: white"
      );
      $(".show-hide-profile").attr("style", "background:#222;");
      $(".user-username").css("color", "#eee");
      $("header").css("box-shadow", "0 3px 10px 0.3px #000");
      $("footer").css("box-shadow", "0 3px 10px 0.3px #000");
      $(
        ".user-comments, .reply_author-comments, .comment_author-comments"
      ).attr("style", "background: #222");
      $(".post-body").css("box-shadow", "0 3px 10px 0.3px #000");
      $(".container").attr(
        "style",
        "background-color:#222; box-shadow: 0 1px 8px 0.5px #000"
      );
    } else {
      $(".show-hide-profile").attr("style", "background:whitesmoke;");
      $(document.body).attr("style", "background:initial; color: initial");
      $(".user-username").css("color", "initial");
      $(".container").attr(
        "style",
        "background-color:#fff; box-shadow: 0 1px 8px 0.5px #ccc"
      );
      $(".post-body").css("box-shadow", "0 3px 10px 0.3px #ccc");
      $("header").css("box-shadow", "unset");
      $("footer").css("box-shadow", "unset");
      $(
        ".user-comments, .reply_author-comments, .comment_author-comments"
      ).attr("style", "background:rgba(210, 210, 210, 0.5)");
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
      code = parsingStyles(p, /(?<=`) +|(?!`)\n|(`(?=\S+)[^`]+`)/gm, "`"),
      linkText = p.match(/((https|http):\/\/)?(\w+|\d+)\.\w+(\S+)?/gim);
    p = p.replace(/</gim, "&lt;").replace(/>/gim, "&gt;");
    for (let index = 0; index < splitter.length; index++)
      p = p.replace(
        splitter[index],
        `<strong style="color: unset; font-weight: 550;">${splitter[index].replace(
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
    if (linkText)
      for (let index = 0; index < linkText.length; index++) {
        if (linkText[index]) {
          let handleLinkProtocol = undefined;
          if (
            linkText[index].includes("https://") ||
            linkText[index].includes("http://") ||
            linkText[index].includes("ftps://") ||
            linkText[index].includes("ftp://")
          ) {
            handleLinkProtocol = linkText[index];
          } else
            handleLinkProtocol =
              "https://" + linkText[index].trimStart().trimEnd();

          p = p.replace(
            linkText[index],
            `<a href='${handleLinkProtocol}' target='_blank' referrerpolicy='no-referrer'>${linkText[index]}</a>`
          );
        }
      }

    $(el).html(p);
  });
  $(".preview").click(() => {
    $(".preview-user-image").css("display", "grid");
  });
  $(".stop-preview").click(() => {
    $(".preview-user-image").css("display", "none");
  });

  // Show or hide profile info
  $(".other-user-profile #view-user-profile").click(() => {
    $(".show-hide-profile").css("display", "grid");
  });
  $(".show-hide-profile #view-user-profile").click(() => {
    $(".show-hide-profile").css("display", "none");
  });
});
