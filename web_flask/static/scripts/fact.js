var limit = 3;
$.ajax({
  method: "GET",
  url: "https://api.api-ninjas.com/v1/facts?limit=100",
  headers: { "X-Api-Key": "/49X+XUEgvclsat8fqQmkA==hPESkzB0AYngwPf0" },
  contentType: "application/json",
  success: function (result) {
    console.log(result);
  },
  error: function ajaxError(jqXHR) {
    console.error("Error: ", jqXHR.responseText);
  },
});
