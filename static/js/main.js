(function ($) {
  "use strict";

  Chart.defaults.color = "#93856cff";
  Chart.defaults.borderColor = "#000000";

  var element = document.getElementById("message-chart");
  if (element) {
    var ctx2 = element.getContext("2d");

    var totalMessages = document.getElementById("total-messages").value;
    var moderatedMessages = document.getElementById("moderated-messages").value;

    new Chart(ctx2, {
      type: "bar",
      data: {
        labels: ["Összes üzenet", "Moderált üzenetek"],
        datasets: [
          {
            label: "Darabszám",
            data: [totalMessages, moderatedMessages],
            backgroundColor: [
              "rgba(245, 155, 63, .7)",
              "rgba(245, 155, 63, .5)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
})(jQuery);
