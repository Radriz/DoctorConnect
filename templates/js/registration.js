document.getElementById("speciality").addEventListener("change", function() {
    const speciality = document.getElementById("speciality").value;
    if (speciality=="doctor"){
        document.getElementById("clinic_div").style.display = "block";
    }
    else {
        document.getElementById("clinic_div").style.display = "none";
    }
})