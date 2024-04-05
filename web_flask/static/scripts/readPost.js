window.onload = () => {
  const sys = speechSynthesis;
  if (sys) {
      let text = $("article h1").text() + $("article p").text();
      let txt = new SpeechSynthesisUtterance(text);
      txt.voice = sys.getVoices()[0];
      txt.volume = 1;
      txt.onend = () => {
        $("#play-btn i").toggleClass("fa-play-circle fa-volume-up");
      };
      // Play the post
      $("#play-btn").on("click", () => {
        window.speechSynthesis.speak(txt);
        $("#play-btn i").toggleClass("fa-play-circle fa-volume-up");
        if ($("#play-btn i").hasClass("fa-play-circle") || window.speechSynthesis.paused) {
          window.speechSynthesis.resume();
		alert(sys.paused)
        }
        if ($("#play-btn i").hasClass("fa-volume-up")) {
          window.speechSynthesis.pause();
        }
        // Stop the playing
        if (window.speechSynthesis.speaking) {
          $("#stop-btn").attr("disabled", false);
          $("#stop-btn").on("click", () => {
            window.speechSynthesis.cancel();
            $("#stop-btn").attr("disabled", true);
            $("#play-btn i").toggleClass("fa-volume-up fa-play-circle");
          });
        }
      });
  } else {
	  console.log("This browser doesn't support Reading Mode!");
	  
	  $('#play-btn').css('display', 'none')
	  $('#stop-btn').css('display', 'none')
  }
/*window.onbeforeunload = () => {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
  };*/
}

// Share buttons
/*$(function () {
  $("#live").jsSocials({
    url: "127.0.0.1:5500/" + window.location.href,
    text: $("#post-title").text(),
    showLabel: false,
    shares: [
      { share: "email", logo: "fa fa-envelope" },
      { share: "twitter", logo: "fab fa-twitter" },
      { share: "facebook", logo: "fab fa-facebook" },
      { share: "linkedin", logo: "fab fa-linkedin" },
      { share: "whatsapp", logo: "fab fa-whatsapp" },
      "messenger",
      "telegram",
    ],
  });
})*/
  // Confirm post deletion
  $("#delete-question-btn").click(() => {
    return confirm("Are you sure about deleting this comment?") ? true : false;
  });
