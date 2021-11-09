$(document).ready(function () {

  // variable declaration
  var usersTable;
  var usersDataArray = [];
  // datatable initialization
  if ($("#users-list-datatable").length > 0) {
    usersTable = $("#users-list-datatable").DataTable({
      responsive: true,
      'columnDefs': [{
        "orderable": false,
        "targets": [0, 1, 2, 3, 4, 5]
      }]
    });
  };
  // on click selected users data from table(page named page-users-list)
  // to store into local storage to get rendered on second page named page-users-view
  $(document).on("click", "#users-list-datatable tr", function () {
    $(this).find("td").each(function () {
      usersDataArray.push($(this).text().trim())
    })

    localStorage.setItem("usersJoinAt", usersDataArray[6]);
  })
  // page users list verified filter
  $("#users-list-join-at").on("change", function () {
    var usersVerifiedSelect = $("#users-list-join_at").val();
    usersTable.search(usersVerifiedSelect).draw();
  });

  // Input, Select, Textarea validations except submit button validation initialization
  if ($(".users-edit").length > 0) {
    $("#accountForm, #infotabForm").validate({
      rules: {
        username: {
          required: true,
          minlength: 5
        },
        name: {
          required: true
        },
        email: {
          required: true
        },
        datepicker: {
          required: true
        },
        address: {
          required: true
        }
      },
      errorElement: 'div'
    });
    $("#infotabForm").validate({
      rules: {
        datepicker: {
          required: true
        },
        address: {
          required: true
        }
      },
      errorElement: 'div'
    });
  }
});