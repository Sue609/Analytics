// script.js

document.getElementById("analysis_method").addEventListener("change", function() {
    var analysisMethod = this.value;
    var descriptiveOptions = document.getElementById("descriptive_options");

    if (analysisMethod === "descriptive") {
        descriptiveOptions.style.display = "block";
    } else {
        descriptiveOptions.style.display = "none";
        document.getElementById("histogram_options").style.display = "none";
    }
});

document.getElementById("descriptive_option").addEventListener("change", function() {
    var descriptiveOption = this.value;
    var histogramOptions = document.getElementById("histogram_options");

    if (descriptiveOption === "histogram") {
        histogramOptions.style.display = "block";
    } else {
        histogramOptions.style.display = "none";
    }
});