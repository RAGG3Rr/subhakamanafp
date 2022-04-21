jQuery(function ($) {
    $(document).ready(function () {
        $("#id_main_category").change(function () {
            const url = '/subcategories/';
            const main_category_id = $(this).val();
            $.ajax({
                url: url,
                data: {
                    'main_category_id': main_category_id
                },
                success: function (data) {
                    let html_data = '<option value="">--------------</option>';

                    data.forEach(function (sub_dropdown) {
                        html_data += `<option value="${sub_dropdown.id}">${sub_dropdown.sub_category}</option>`
                    });
                    $("#id_sub_category").html(html_data);
                },
                error: function (e) {
                    console.error(JSON.stringify(e));
                },
            });
        });

        $("#id_sub_category").change(function () {
            const url = '/specificcategories/';
            const sub_category_id = $(this).val();
            $.ajax({
                url: url,
                data: {
                    'sub_category_id': sub_category_id
                },
                success: function (data) {
                    let html_data = '<option value="">--------------</option>';
                    data.forEach(function (specific_dropdown) {
                        html_data += `<option value="${specific_dropdown.id}">${specific_dropdown.specific_category}</option>`
                    });
                    $("#id_specific_category").html(html_data);
                },
                error: function (e) {
                    console.error(JSON.stringify(e));
                },
            })
        });
    });
});