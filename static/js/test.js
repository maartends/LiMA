require([
         "dojo/_base/Color",
         "dojo/request/xhr",
         "dojox/charting/DataChart",
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
         "dojo/store/util/QueryResults",
         "dojox/charting/themes/MM_Charts",
         "dojo/ready"
         ],
         function(Color, xhr, DataChart, ItemFileReadStore, Memory, ObjectStore, DataStore, JsonRest, StoreSeries, DataSeries, Default, Columns, Lines, Tooltip, QueryResults, MM_Charts, ready) {

    ready(function() {

        function MM_Chart(period) {
            this.name = period;
            this.chart_name = 'chart' + period + 'Omzet';
            this.store_url = '/json_auctions/charts/' + period;
            var store;
            this.store = store;
            this.store_query = {};
            this.store_query[period] = '*';
            this.period_max_val = 10000;
            // get json data via xhr
            var dataStore;
            var storeItems;
            xhr(this.store_url, {
                method: 'GET',
                handleAs: 'json'
            })
            .then(function (data) {
                this.store =  new Memory({
                    data: data,
                    item_count: data.item_count,
                });
                console.log("store Memory", this.store);
                this.chart = new DataChart(this.chart_name, {comparative:true, title: this.chart_name }).
                addAxis("y", {vertical:true, min:0, max:this.period_max_val, microTicks:false, minorTicks:false, majorTickStep:1000}).
                addAxis("x", {natural: true, dropLabels: false }).
                addPlot("default", {type: Columns, hAxis: "x", vAxis: "y", hMajorLines: true}).
                addSeries("y", new StoreSeries(this.store, this.store_query, {y: "omzet", x: this.period, tooltip: "omzet"} )).
                setTheme(MM_Charts).render();
                console.log("this.chart:", this.chart);
            }, function (err) {
                content = "<p>error: </p><p>" + err.response.text + "</p>";
                mm_popup_dialog.set("content",  content);
                mm_popup_dialog.set("title", 'Error');
            });
        };

        week = new MM_Chart('week');

    });

});