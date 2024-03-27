let questionIDs = $(".question-id"),
  postIDs = $(".post-ids"),
  editPostIDs = $(".edit-post-ids");

function storeID(classID, newID, getConfirmed = false) {
  $.each($(classID), function (indexInArray, form) {
    $(form).submit(function (e) {
      //e.preventDefault();
      $(newID[indexInArray]).val($(questionIDs[indexInArray]).text());
      if (getConfirmed) return confirm("Are you sure?") ? true : false;
    });
  });
}
storeID(".delete_form", postIDs, true);
// $("#update-image").submit((e) => {
//   if ($("#image").val() === "") {
//     $("p#incorrect-pwd").text("Password does not match!");
//     e.preventDefault();
//   }
// });
