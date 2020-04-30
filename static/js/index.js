var current_table = null;
var page = 1;
var limit = 50;
var total = 100;
var editor_pk = 'undefined';
var editor_pk_value = null;

var temp_column_data = null;


var reg_name = new RegExp("\{name\}", "g");
var reg_value = new RegExp("\{value\}", "g");

function refresh() {
    $.ajax({
        type: "GET",
        url: "/data",
        dataType: "json",
        data: {"table_name": current_table, "page": page, "limit": limit, "where": $("#id_where").val()},
        success: function (result) {

            var title = null;

            var html = [];

            total = result.count;
            refreshPager();

            editor_pk = result['PK']


            html.push('<table class="table table-bordered table-hover" style="margin-left: 0;">');

            if (result.items.length > 0 && title == null) {

                html.push(['<thead ><tr class="active">']);
                html.push("<th>action</th>");
                for (col in result.items[0]) {
                    html.push("<th>" + col + "</th>")
                }
                html.push(' </tr></thead><tbody>');
            }

            $.each(result.items, function (index, item) {
                html.push('<tr>');
                html.push("<td><button class='btn' style='background-color: inherit' onclick='showEditor(\"" + item[result['PK']] + "\")'><span class=\"glyphicon glyphicon-edit\" aria-hidden=\"true\"></span></button></td>");
                for (col in item) {
                    var value = item[col];
                    if (typeof (item[col]) == 'string' && item[col].startsWith('http')) {
                        if (item[col].endsWith(".jpg") || item[col].endsWith(".png")) {
                            value = "<img src= \"" + item[col] + "\" height='100px'/>";
                        } else {
                            value = "<a href=\"" + item[col] + "\" target='_blank'>连接</a>";
                        }
                        html.push('<td width="50px">' + value + '</td>');
                    } else {
                        html.push('<td>' + (value == null ? " - " : value) + '</td>');
                    }
                }
                html.push('</tr>');
            });

            html.push('</tbody></table>');

            $("#data-container").html(html.join(''));
        },
        error: function (req, status, err) {

            $("#data-container").html("<div style='color: red'>" + req.responseJSON['errors'] + "</div>");
        }
    });
}

function refreshPager() {

    var html = [];

    start = page - 5 > 0 ? page - 5 : 1;

    for (var index = start, count = 0; index <= Math.ceil(total / limit) && count <= 15; index++, count++) {
        html.push("<button class=\"btn btn-default\" onclick='to_N_page(" + index + ")'> " + index + " </button>")
    }

    $("#pager-container-bottom").html(html.join(" "));
    $("#pager-container-top").html(html.join(" "));
}

function setTablename(tablename) {
    current_table = tablename;
    page = 1;
    $("#id_table_name").html(tablename);
    refresh();

    $("#_id_table_ul li").removeClass();
    $("#_id_table_" + tablename).addClass("active");
}

function to_first_page() {
    page = 1;
    refresh();
}

function to_previous_page() {
    page -= 1;
    if (page < 1) {
        page = 1;
    }
    refresh();
}

function to_N_page(n) {
    page = n;
    refresh();
}


function to_next_page() {
    page += 1;
    if (page < 1) {
        page = 1;
    }
    refresh();
}

function to_end() {
    page = Math.ceil(total / limit);
    refresh();
}

function click_filter() {
    $('#id_filter').modal('toggle');
    refresh();
}


function showEditor(value) {
    if (value == 'undefined') {
        console.debug("undefined")
    }

    editor_pk_value = value;

    $.getJSON("/column_data", {
        "table_name": current_table,
        "column": editor_pk,
        "value": value
    }, function (result, status, xhr) {
        if (result.length == 0) {
            return;
        }
        temp_column_data = result[0];
        var item_str = "<div class='form-group'><label for=_id_{name}>{name}</label><input type=text class=form-control id=_id_{name} value='{value}'> </div>";


        console.debug(item_str);
        var html = [];
        html.push("<form>");
        for (name in temp_column_data) {

            html.push(item_str.replace(reg_name, name).replace(reg_value, temp_column_data[name]))
        }
        html.push("</form>");

        $("#id_editor_content").html(html.join(""));
        $("#id_editor").modal('toggle');
    });
}

function update_this_pk() {
    var m = {};

    for (column_name in temp_column_data) {
        var _value = $("#_id_{name}".replace(reg_name, column_name)).val();
        if (_value != String(temp_column_data[column_name])) {
            m[column_name] = _value;
            console.debug(_value);
        }
    }

    $.get("/column_update", {
        "table_name": current_table,
        "name": editor_pk,
        "value": editor_pk_value,
        "columns": JSON.stringify(m)
    }, function (data) {
        if (data == 'SUCCESS') {
            $("#id_editor").modal('toggle');
        } else {
            alert("error");
        }
    });
}

//init
refresh();