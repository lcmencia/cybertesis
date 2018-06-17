$(document).ready(function() {
   var $faculty_select = $("#faculty_select");
   var faculty_len = facultyList.length;
   for (var i = 0; i < faculty_len; i++){
       $faculty_select.append($("<option></option>").attr("value", facultyList[i].id).text(facultyList[i].name));
   }

   var faculty_selected = $("#faculty_select").val();
   var $career_select = $("#career_select");
   var career_len = careerList.length;
   for (var i = 0; i < career_len; i++){
       if(faculty_selected==careerList[i].fk){
           $career_select.append($("<option></option>").attr("value", careerList[i].id).text(careerList[i].name));
       }
   }

    $faculty_select.on('change', function() {
       var $career_select = $("#career_select");
       $career_select.empty();
       var faculty_selected = $(this).val();
       for (var i = 0; i < career_len; i++){
           if(faculty_selected==careerList[i].fk){
               $career_select.append($("<option></option>").attr("value", careerList[i].id).text(careerList[i].name));
           }
       }
    });

    var $subcategory_select = $("#subcategory_select");
    var subcategory_len = subcategoryList.length;
    for (var i = 0; i < subcategory_len; i++){
       $subcategory_select.append($("<option></option>").attr("value", subcategoryList[i].id).text(subcategoryList[i].name));
    }
});