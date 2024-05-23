var fittingCheckBox = document.getElementById('fitting_done');
var doneCheckBox = document.getElementById('done');

fittingCheckBox.addEventListener('change', function() {
document.getElementById('fitting_done_form').submit();
});
doneCheckBox.addEventListener('change', function() {
document.getElementById('done_form').submit();
});