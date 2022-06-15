$(document).ready(function (e) {
    var percentageComplete = 0.7;
    var strokeDashOffsetValue = 100 - (percentageComplete * 100);
    var progressBar = $(".js-progress-bar");
    progressBar.css("stroke-dashoffset", strokeDashOffsetValue);
});
