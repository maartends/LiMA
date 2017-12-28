/*
 * Dojo
 * Author: Maarten De Schrijver
*/

/*
 * Out of ready stuff
 */
mm_datagrid_formatters = {
    formatCurrency: function(value, rowIndex) {
        return "€ " + value;
    },
    formatPercent: function(value, rowIndex) {
        return value + " %";
    },
    formatMailLink: function(value, rowIndex) {
        return "<a href='mailto:" + value + "'>" + value + "</a>";
    },
    formatRowPopup: function(value, rowIndex) {
        var rowdata = this.grid.getItem(rowIndex);
        if (dijit.byId('show_grid').name == 'customer_show_grid') {
            var urlPath = '/CustomerManager/customer/' + rowdata.clang_id + '/view';
        } else if (dijit.byId('show_grid').name == 'auction_show_grid') {
            var urlPath = '/AuctionManager/auction/' + rowdata.veiling_id + '/view';
        }
        var onClick = 'mm_clicked("' + urlPath + '")';
        return "<a href='#' class='mm_dialog' title='View' onClick='" + onClick + "'>" + value + "</a>";
    },
};

/*
 * Dojo specific stuff
 */
require([
        "dojo",
        "dojo/parser",
        "dojo/ready",
        "dojo/query",
        "dojo/request/xhr",
        "dojo/on",
        "dojo/json",
        "dojo/topic",
        "dojo/dom",
        "dojo/dom-construct",
        "dojo/dom-attr",
        "dijit/Dialog",
        "dijit/form/Form",
        "dijit/form/Button",
        "dijit/form/ValidationTextBox",
        "dijit/form/TextBox",
        "dijit/form/Select",
        "dijit/form/FilteringSelect",
        "dijit/form/DateTextBox",
        "dojox/validate",
        "dijit/layout/TabContainer",
        "dijit/layout/BorderContainer",
        "dijit/layout/AccordionContainer",
        "dijit/layout/ContentPane",
        "dijit/MenuBar",
        "dijit/PopupMenuBarItem",
        "dijit/DropDownMenu",
        "dijit/Menu",
        "dijit/MenuItem",
        "dijit/MenuSeparator",
        "dijit/PopupMenuItem",
        "dojo/data/ItemFileReadStore",
        "dijit/tree/ForestStoreModel",
        "dijit/Tree",
        "dijit/Calendar",
        "dojox/calendar/Calendar",
        "dojo/store/JsonRest",
        "dojox/widget/Toaster",
        "dijit/registry",
        "dojox/grid/EnhancedGrid",
        "dojox/grid/enhanced/plugins/Menu",
        "dojo/domReady!",
         ],
    function(require, parser, ready, query, xhr, on, JSON, dom, domConstruct, domAttr, ItemFileReadStore, ForestStoreModel, Dialog, Button, topic, Toaster, registry, lang, EnhancedGrid){

        update_veilingen_db = function() {
            var btn = new dijit.form.Button({
                label: "Ok",
                type: "submit",
                name: "submit",
            });
            var box = new dijit.form.TextBox({
                name: "url",
                placeHolder: "URL",
                label: "URL",
            });
            var f = new dijit.form.Form({
                id: 'update_veilingen_form',
                method: "POST",
                action: "/action/update_veilingen_db",
                onSubmit: function(evt) {
                    dojo.stopEvent(evt);
                    var xhrArgs = {
                        form: 'update_veilingen_form',
                        handleAs: "json",
                        load: function(data){
                            var content = "";
                            content += "<h2>Succes</h2>";
                            content += "<p>" + data.action + "</p>";
                            content += "<p>" + data.response + "</p>";
                            content += "<p>Table recreated: tmp_veilingen</p>";
                            content += "<p>Tmp file written to: /tmp/sheet2copy.csv</p>";
                            content += "<p>You can close this window.</p>";
                            dojo.byId("progresstext").innerHTML = content;
                        },
                        error: function(error){
                            dojo.byId("progresstext").innerHTML = error;
                            console.log(error);
                        }
                    };
                    dojo.byId("progresstext").innerHTML = "Busy...";
                    // Call the asynchronous xhrPost
                    var deferred = dojo.xhrPost(xhrArgs);
                },
            });
            var dialog = new dijit.Dialog({
                title : "Update veilingen db",
                content : "<p>Geef de URL naar de CSV in.</p>\n<p id='progresstext'></p>",
            });
            dojo.place(box.domNode, f.containerNode);
            dojo.place(btn.domNode, f.containerNode);
            dojo.place(f.domNode, dialog.containerNode);
            dialog.show();
        };
/*
        update_defaulters_grid = function(n) {
            update_sub_func(n);
        }
*/

        function init() {

            var surprise = query("#surprise");
            var h1 = dojo.subscribe("log_mm_messages", function(){
                console.log("received:", arguments);
                h1.remove();
            });
            var h2 = dojo.subscribe("testMessageTopic", function(e){
                //~ dijit.byId('first_toaster').setContent(e.message, e.type, e.duration);
                //~ dijit.byId('first_toaster').show();
                h2.remove();
            });
            on(surprise, "click", function() {
                dojo.publish("log_mm_messages", "one", "two");
                dojo.publish("testMessageTopic", [
                 {
                   message: "Heb je al koffie gedronken?",
                   type: "message",
                   duration: 4000
                 }
                ]);
            });

            var flash = query("#flash");
            //~ if (flash) {
                //~ dojo.publish("testMessageTopic", [
                 //~ {
                   //~ message: "Logged in!",
                   //~ type: "message",
                   //~ duration: 4000
                 //~ }
                //~ ]);
            //~ };

            var dialog_content = '\
            <div class="dijitDialogPaneContentArea">${c}</div>\
            <div class="dijitDialogPaneActionBar">\
                <button id="ABdialog1button1" data-dojo-type="dijit/form/Button" data-dojo-props=\'type:"submit" \'>OK</button>\
                <button id="ABdialog1button2" data-dojo-type="dijit/form/Button" data-dojo-props=\'type:"button", onClick:function(){ dijit.byId("mm_popup_dialog").onCancel(); }\'>Cancel</button>\
            </div>\
            '

            var mm_dialog = query(".mm_dialog");
            on(mm_dialog, "click", function(evt) {
                evt.preventDefault();
                var t = evt.target;
                xhr(t.href, {
                    method: 'GET',
                    handleAs: 'text'
                })
                .then(function (data) {
                    mm_popup_dialog.set("content", data);
                    mm_popup_dialog.set("title", t.title);
                }, function (err) {
                    content = "<p>error: <p>" + err.response.text + "</p></p>";
                    mm_popup_dialog.set("content",  content);
                    mm_popup_dialog.set("title", 'error');
                });
                mm_popup_dialog.show();
            });

            query("#addline").on("click", function(evt){
                evt.preventDefault();
                var row = new dijit.form.ValidationTextBox( {
                    id : "emailbox",
                    selectOnClick : true,
                    name : "emailbox",
                    trim : true,
                    required : true,
                    invalidMessage : "Dit is geen correct emailadres"
                    } );
                row.placeAt("invite_list");
                row.startup();
            });

            query(".ajaxClick").on("click", function(evt){
                evt.preventDefault();
                var t = evt.target;
                mm_dialog_alert.set("href",  t.href);
                mm_dialog_alert.set("title",  t.title);
                mm_dialog_alert.show();
            });

            query("#flash").on("click", function(evt){
                evt.preventDefault();
                var t = evt.target;
                dojo.destroy(t);
            });

            var ajaxclickednode = query(".ajaxclick");
            on(ajaxclickednode, "click", function(evt){
                evt.preventDefault();
                var t = evt.target;
                console.log(t.href);
                var id = dojo.getAttr(t, "data-ezine-id");
                console.log(id);
                var btn = new dijit.form.Button({
                    label: "Ok",
                    type: "submit",
                    name: "submit",
                });
                var box = new dijit.form.TextBox({
                    name: "id",
                    type: "hidden",
                    value: id,
                });
                var f = new dijit.form.Form({
                    id: 'confirm_form',
                    method: "POST",
                    action: t.href,
                    onSubmit: function(evt) {
                        dojo.stopEvent(evt);
                        var xhrArgs = {
                            form: 'confirm_form',
                            handleAs: "json",
                            load: function(data){
                                var content = "";
                                content += "<h2>Succes</h2>";
                                content += "<p>" + data.action + "</p>";
                                content += "<p>" + data.response + "</p>";
                                content += "<p>You can close this window.</p>";
                                console.log(data);
                                dojo.byId("progresstext").innerHTML = content;
                            },
                            error: function(error){
                                dojo.byId("progresstext").innerHTML = error;
                                console.log(error);
                            }
                        };
                        dojo.byId("progresstext").innerHTML = "Busy... please wait.";
                        // Call the asynchronous xhrPost
                        var deferred = dojo.xhrPost(xhrArgs);
                    },
                });
                var dialog = new dijit.Dialog({
                    title : "Upload ezine to Clang",
                    content : "<p>Upload ezine to Clang?</p>\n<p id='progresstext'></p>",
                });
                dojo.place(box.domNode, f.containerNode);
                dojo.place(btn.domNode, f.containerNode);
                dojo.place(f.domNode, dialog.containerNode);
                dialog.show();
            });

            mm_clicked = function(href) {
                console.log(href);
                window.history.pushState('','', href);
                mm_popup_dialog.set("href",  href);
                mm_popup_dialog.set("title", 'Dialog');
                mm_popup_dialog.show();
            };

            update_defaulters_grid = function(n) {
                var url = "/json_auctions/defaulters/" + n;
                xhr(url, {
                    handleAs: 'json',
                    method: 'GET'
                })
                .then(function (data) {
                    if (data.items.length == 0) {
                        dojo.publish("testMessageTopic", [
                         {
                           message: "Sorry, no records found for " + n + " days ago",
                           type: "message",
                           duration: 4000
                         }
                        ]);
                    } else {
                        defaulters = new dojo.data.ItemFileReadStore({data: data});
                        show_grid = dijit.byId('defaulters_show_grid');
                        show_grid.setStore(defaulters);
                    };
                }, function (err) {
                    dojo.publish("testMessageTopic", [
                         {
                           message: "An error occured " + err.response.text,
                           type: "message",
                           duration: 4000
                         }
                    ]);
                });
            };

            /* Grid functions */

            viewRowDataPopup = function(evt) {
                var item = evt.grid.getItem(evt.rowIndex);
                if (evt.grid.name == 'customer_show_grid') {
                    var urlPath = '/AuctionManager/auction/' + evt.grid.store.getValue(item, 'veiling_id') + '/view';
                } else if (evt.grid.name == 'auction_show_grid') {
                    var urlPath = '/CustomerManager/customer/' + evt.grid.store.getValue(item, 'clang_id') + '/view';
                }
                mm_clicked(urlPath);
            };

            viewRowData = function(evt) {
                var item = evt.grid.getItem(evt.rowIndex);
                var urlPath = '/json_auctions/search/'
                if (evt.grid.name == 'auction_search_grid') {
                    urlPath += 'customer';
                } else if (evt.grid.name == 'customer_search_grid') {
                    urlPath += 'auction';
                }
                var clang_id = evt.grid.store.getValue(item, 'clang_id');
                xhr(urlPath, {
                    query: {'clang_id': clang_id },
                    handleAs: 'json'
                })
                .then(function (data) {
                    /*set up datastore */
                    auctionstore = new dojo.data.ItemFileReadStore({data: data});
                    dijit.byId('show_grid').setStore(auctionstore);
                }, function (err) {
                    content = "<p>error: <p>" + err.response.text + "</p></p>";
                    mm_popup_dialog.set("content",  content);
                    mm_popup_dialog.set("title", id);
                    mm_popup_dialog.show();
                });
            };

            ezines = new dojo.store.JsonRest({
                target:"json/Ezine"
            });

            // Grid context menu functions
            //~ var show_grid = dijit.byId('show_grid');
            //~ show_grid.onRowContextMenu = function(e) {
                //~ cellNode = e.cellNode;
                //~ console.log(e.rowIndex);
                //~ viewRowData = function() {
                    //~ console.log(cellNode);
                //~ };
            //~ };
            //~ viewRowData = function(e) {
                //~ dojo.connect(show_grid, 'onRowContextMenu', function(e){
                    //~ var rowIndex = e.rowIndex;
                    //~ var colIndex = e.cellIndex;
                //~ });
                //~ console.log(e.cellNode);
            //~ };

        }; // init

        ready(init);

    });

require([
         "dojo/_base/Color",
         "dojo/_base/lang",
         "dojo/request/xhr",
         "dojo/currency",
         "dojomm/charting/DataChart",
         "dojomm/charting/themes/MM_Charts",
         "dojo/data/ItemFileReadStore",
         "dojo/store/Memory",
         "dojo/data/ObjectStore",
         "dojo/store/DataStore",
         "dojo/store/JsonRest",
         "dojox/charting/StoreSeries",
         "dojox/charting/DataSeries",
         "dojox/charting/axis2d/Default",
         "dojox/charting/plot2d/Columns",
         "dojox/charting/plot2d/Lines",
         "dojox/charting/action2d/Tooltip",
         "dojox/charting/action2d/Highlight",
         "dojo/store/util/QueryResults",
         "dojo/ready"
         ],
         function(Color, lang, xhr, currency, DataChart, ItemFileReadStore, Memory, ObjectStore, DataStore, JsonRest, StoreSeries, DataSeries, Default, Columns, Lines, Tooltip, Highlight, QueryResults, MM_Charts, ready) {

    ready(function() {

        function MM_Chart(period, type) {
            this.period = period;
            this.type = type;
            this.chartName = 'chart_' + period + '_' + type;
            this.chartHumanName = type + '/' + period;
            this.storeUrl = '/json_auctions/charts/' + period;
            this.store = null;
            this.storeQuery = {};
            this.storeQuery[period] = '*';
            this.periodMaxVals = {};
            this.seriesMaxVal = null;
            this.djChart = new DataChart(this.chartName, {comparative:true, title:this.chartHumanName}).
                addAxis("x", {natural: true, dropLabels: false }).
                addPlot("default", {type: Columns, hAxis: "x", vAxis: "y", hMajorLines: true}).
                setTheme(MM_Charts);
        };

        function CalcMajorTickStep(maxVal, n) {
            return dojo.number.round(Math.pow(10, Math.ceil(Math.log(maxVal)/Math.LN10))/n);
        }

        function addTooltip(chart) {
            if (chart.type == 'omzet') {
                new Tooltip(chart.djChart, "default", {
                    text : function(o) {
                    return chart.period + " " + (parseInt(o.x, 10)+1) + " : " + currency.format(o.y, {currency : "EUR", places : 0});
                }});
            } else {
                new Tooltip(chart.djChart, "default", {
                    text : function(o) {
                    return chart.period + " " + (parseInt(o.x, 10)+1) + " : " + o.y + " verkocht";
                }});
            }
        };

        processData = function(data) {

        };

        renderCharts = function() {

            var charts = {};
            charts.weekn = new MM_Chart('week', 'n');
            charts.monthn = new MM_Chart('month', 'n');
            charts.weekomzet = new MM_Chart('week', 'omzet');
            charts.monthomzet = new MM_Chart('month', 'omzet');

            console.log("1", charts);

                xhr(charts.weekn.storeUrl, {
                    method: 'GET',
                    handleAs: 'json'
                }).then(function (data) {
                    charts.weekn.store =  new Memory({
                        data: data,
                        item_count: data.item_count,
                    });
                    charts.weekn.periodMaxVals = data.max_values;
                    charts.weekn.seriesMaxVal = data.max_values[charts.weekn.type];
                    console.log("2", charts.weekn);
                    charts.weekn.djChart.
                        addAxis("y", {vertical:true, min:0, max:charts.weekn.seriesMaxVal, microTicks:false, minorTicks:false, majorTickStep: CalcMajorTickStep(charts.weekn.seriesMaxVal, 10)}).
                        addSeries("y", new StoreSeries(charts.weekn.store, charts.weekn.storeQuery, {y: charts.weekn.type, x: charts.weekn.period, tooltip: charts.weekn.type} ));
                    addTooltip(charts.weekn);
                    charts.weekn.djChart.render();
                    console.log("3", charts.weekn);
                }, function (err) {
                    content = "<p>error: </p><p>" + err.response.text + "</p>";
                    mm_popup_dialog.set("content",  content);
                    mm_popup_dialog.set("title", 'Error');
                });

                xhr(charts.monthn.storeUrl, {
                    method: 'GET',
                    handleAs: 'json'
                }).then(function (data) {
                    charts.monthn.store =  new Memory({
                        data: data,
                        item_count: data.item_count,
                    });
                    charts.monthn.periodMaxVals = data.max_values;
                    charts.monthn.seriesMaxVal = data.max_values[charts.monthn.type];
                    console.log("2", charts.monthn);
                    charts.monthn.djChart.
                        addAxis("y", {vertical:true, min:0, max:charts.monthn.seriesMaxVal, microTicks:false, minorTicks:false, majorTickStep: CalcMajorTickStep(charts.monthn.seriesMaxVal, 10)}).
                        addSeries("y", new StoreSeries(charts.monthn.store, charts.monthn.storeQuery, {y: charts.monthn.type, x: charts.monthn.period, tooltip: charts.monthn.type} ));
                    addTooltip(charts.monthn);
                    charts.monthn.djChart.render();
                    console.log("3", charts.monthn);
                }, function (err) {
                    content = "<p>error: </p><p>" + err.response.text + "</p>";
                    mm_popup_dialog.set("content",  content);
                    mm_popup_dialog.set("title", 'Error');
                });

                xhr(charts.weekomzet.storeUrl, {
                    method: 'GET',
                    handleAs: 'json'
                }).then(function (data) {
                    charts.weekomzet.store =  new Memory({
                        data: data,
                        item_count: data.item_count,
                    });
                    charts.weekomzet.periodMaxVals = data.max_values;
                    charts.weekomzet.seriesMaxVal = data.max_values[charts.weekomzet.type];
                    console.log("2", charts.weekomzet);
                    charts.weekomzet.djChart.
                        addAxis("y", {vertical:true, min:0, max:charts.weekomzet.seriesMaxVal, microTicks:false, minorTicks:false, majorTickStep: CalcMajorTickStep(charts.weekomzet.seriesMaxVal, 10)}).
                        addSeries("y", new StoreSeries(charts.weekomzet.store, charts.weekomzet.storeQuery, {y: charts.weekomzet.type, x: charts.weekomzet.period, tooltip: charts.weekomzet.type} ));
                    addTooltip(charts.weekomzet);
                    charts.weekomzet.djChart.render();
                    console.log("3", charts.weekomzet);
                }, function (err) {
                    content = "<p>error: </p><p>" + err.response.text + "</p>";
                    mm_popup_dialog.set("content",  content);
                    mm_popup_dialog.set("title", 'Error');
                });

                xhr(charts.monthomzet.storeUrl, {
                    method: 'GET',
                    handleAs: 'json'
                }).then(function (data) {
                    charts.monthomzet.store =  new Memory({
                        data: data,
                        item_count: data.item_count,
                    });
                    charts.monthomzet.periodMaxVals = data.max_values;
                    charts.monthomzet.seriesMaxVal = data.max_values[charts.monthomzet.type];
                    console.log("2", charts.monthomzet);
                    charts.monthomzet.djChart.
                        addAxis("y", {vertical:true, min:0, max:charts.monthomzet.seriesMaxVal, microTicks:false, minorTicks:false, majorTickStep: CalcMajorTickStep(charts.monthomzet.seriesMaxVal, 10)}).
                        addSeries("y", new StoreSeries(charts.monthomzet.store, charts.monthomzet.storeQuery, {y: charts.monthomzet.type, x: charts.monthomzet.period, tooltip: charts.monthomzet.type} ));
                    addTooltip(charts.monthomzet);
                    charts.monthomzet.djChart.render();
                    console.log("3", charts.monthomzet);
                }, function (err) {
                    content = "<p>error: </p><p>" + err.response.text + "</p>";
                    mm_popup_dialog.set("content",  content);
                    mm_popup_dialog.set("title", 'Error');
                });

        };

    });

});

