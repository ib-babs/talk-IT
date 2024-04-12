window.onload = () => {
  // ======= //

  // Declaring share URLs
  let urlOnly = new URL(window.location.href),
    urlWithTitle = new URL(`${window.location.href}?${$("article h2").text()}`);
  const link_url = [
    "https://facebook.com/sharer/sharer.php?u=" + urlOnly,
    `https://twitter.com/share?url=${urlOnly}&text=${$("article h2").text()}`,
    `whatsapp://send?text=${urlWithTitle}`,
    `tg://msg?text=${urlWithTitle}`,
    "https://www.linkedin.com/shareArticle?mini=true&url=" + urlWithTitle,
  ];

  $.each($("#share-container div a"), function (indexInArray, link) {
    $("#share-container div a")[indexInArray].href = link_url[indexInArray];
  });

  $("#stop-btn i").css("color", "grey");
  const sys = speechSynthesis;
  if (sys) {
    let text = $("article h2").text() + $("article p").text();
    let txt = new SpeechSynthesisUtterance(text);
    txt.voice = sys.getVoices()[0];
    txt.volume = 1;
    txt.onend = () => {
      $("#play-btn i").toggleClass("fa-play-circle fa-volume-up");
      sys.cancel();
    };
    // Play the post
    $("#play-btn").on("click", () => {
      sys.speak(txt);
      $("#play-btn i").toggleClass("fa-play-circle fa-volume-up");
      if ($("#play-btn i").hasClass("fa-play-circle") || sys.paused) {
        sys.resume();
      }
      if ($("#play-btn i").hasClass("fa-volume-up")) {
        sys.pause();
      }
      // Stop the playing
      if (window.speechSynthesis.speaking) {
        $("#stop-btn").attr("disabled", false);
        $("#stop-btn i").css("color", "white");
        $("#stop-btn").on("click", () => {
          window.speechSynthesis.cancel();
          $("#stop-btn").attr("disabled", true);
          $("#stop-btn i").css("color", "grey");
          $("#play-btn i").toggleClass("fa-volume-up fa-play-circle");
        });
      }
    });
  } else {
    console.log("This browser doesn't support Reading Mode!");

    $("#play-btn").css("display", "none");
    $("#stop-btn").css("display", "none");
  }
  window.onbeforeunload = () => {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
  };

  // Confirm post deletion
  $.each($(".delete-post-btn"), function (indexInArray, deleteBtn) {
    $(deleteBtn).click(() => {
      return confirm("Are you sure about deleting this comment?")
        ? true
        : false;
    });
  });

  let prevImgDiv = $("#preview-image"),
    prevImg = $("#preview-image img"),
    trackIndex = 0;

  $.each($(".post-imgs"), function (indexInArray, img) {
    $(img).click(function () {
      trackIndex = indexInArray;
      prevImgDiv.attr("style", "display:block");
      $(prevImg).attr("src", img.src);

      // Previous image
      $("#prev").click(function () {
        if (trackIndex > 0) {
          $("#next").css("color", "blue");
          trackIndex -= 1;
          $(prevImg).attr("src", $(".post-imgs")[trackIndex].src);
        } else $("#prev").css("color", "grey");
      });
      // === //
      // Next image
      $("#next").click(function () {
        if (trackIndex < $(".post-imgs").length - 1) {
          $("#prev").css("color", "blue");
          trackIndex += 1;
          $(prevImg).attr("src", $(".post-imgs")[trackIndex].src);
        } else $("#next").css("color", "grey");
      });
    });
    // === //
  });

  $("#preview-image #back-arrow").click(function () {
    prevImgDiv.css("display", "none");
  });
  // ===== //

  $("#share-post").click(() => {
    $("#share-outer-div, #share-container").css("display", "block");
  });
  $("#share-outer-div").click(() => {
    $("#share-outer-div, #share-container").css("display", "none");
  });
};
