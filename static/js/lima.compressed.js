mm_datagrid_formatters={formatMailLink:function(_1,_2){return "<a href='mailto:"+_1+"'>"+_1+"</a>";},formatRowPopup:function(_3,_4){var _5=this.grid.getItem(_4);if(show_grid.name=="customer_show_grid"){var _6="/CustomerManager/customer/"+_5.clang_id+"/view";}else{if(show_grid.name=="auction_show_grid"){var _6="/AuctionManager/auction/"+_5.veiling_id+"/view";}}var _7="mm_clicked(\""+_6+"\")";return "<a href='#' class='mm_dialog' title='View' onClick='"+_7+"'>"+_3+"</a>";},};require(["dojo","dojo/parser","dojo/ready","dojo/query","dojo/request/xhr","dojo/on","dojo/json","dojo/topic","dojo/dom","dojo/dom-construct","dojo/dom-attr","dijit/Dialog","dijit/form/Form","dijit/form/Button","dijit/form/ValidationTextBox","dijit/form/TextBox","dijit/form/Select","dijit/form/FilteringSelect","dijit/form/DateTextBox","dojox/validate","dijit/layout/TabContainer","dijit/layout/BorderContainer","dijit/layout/AccordionContainer","dijit/layout/ContentPane","dijit/MenuBar","dijit/PopupMenuBarItem","dijit/DropDownMenu","dijit/Menu","dijit/MenuItem","dijit/MenuSeparator","dijit/PopupMenuItem","dojo/data/ItemFileReadStore","dijit/tree/ForestStoreModel","dijit/Tree","dijit/Calendar","dojox/calendar/Calendar","dojo/store/JsonRest","dojox/widget/Toaster","dijit/registry","dojox/grid/EnhancedGrid","dojox/grid/enhanced/plugins/Menu","dojo/domReady!",],function(_8,_9,_a,_b,_c,on,_d,_e,_f,_10,_11,_12,_13,_14,_15,_16,_17,_18,_19){update_veilingen_db=function(){var btn=new dijit.form.Button({label:"Ok",type:"submit",name:"submit",});var box=new dijit.form.TextBox({name:"url",placeHolder:"URL",label:"URL",});var f=new dijit.form.Form({id:"update_veilingen_form",method:"POST",action:"/action/update_veilingen_db",onSubmit:function(evt){dojo.stopEvent(evt);var _1a={form:"update_veilingen_form",handleAs:"json",load:function(_1b){var _1c="";_1c+="<h2>Succes</h2>";_1c+="<p>"+_1b.action+"</p>";_1c+="<p>"+_1b.response+"</p>";_1c+="<p>Table recreated: tmp_veilingen</p>";_1c+="<p>Tmp file written to: /tmp/sheet2copy.csv</p>";_1c+="<p>You can close this window.</p>";console.log(_1b);dojo.byId("progresstext").innerHTML=_1c;},error:function(_1d){dojo.byId("progresstext").innerHTML=_1d;console.log(_1d);}};dojo.byId("progresstext").innerHTML="Busy...";var _1e=dojo.xhrPost(_1a);},});var _1f=new dijit.Dialog({title:"Update veilingen db",content:"<p>Geef de URL naar de CSV in.</p>\n<p id='progresstext'></p>",});dojo.place(box.domNode,f.containerNode);dojo.place(btn.domNode,f.containerNode);dojo.place(f.domNode,_1f.containerNode);_1f.show();};function _20(){var _21=_b("#surprise");var h1=dojo.subscribe("log_mm_messages",function(){console.log("received:",arguments);h1.remove();});var h2=dojo.subscribe("testMessageTopic",function(e){h2.remove();});on(_21,"click",function(){dojo.publish("log_mm_messages","one","two");dojo.publish("testMessageTopic",[{message:"Heb je al koffie gedronken?",type:"message",duration:4000}]);});var _22=_b("#flash");var _23="            <div class=\"dijitDialogPaneContentArea\">${c}</div>            <div class=\"dijitDialogPaneActionBar\">                <button id=\"ABdialog1button1\" data-dojo-type=\"dijit/form/Button\" data-dojo-props='type:\"submit\" '>OK</button>                <button id=\"ABdialog1button2\" data-dojo-type=\"dijit/form/Button\" data-dojo-props='type:\"button\", onClick:function(){ dijit.byId(\"mm_popup_dialog\").onCancel(); }'>Cancel</button>            </div>            ";var _24=_b(".mm_dialog");on(_24,"click",function(evt){evt.preventDefault();var t=evt.target;var w=dijit.getEnclosingWidget(t);_c(t.href,{method:"GET",handleAs:"text"}).then(function(_25){mm_popup_dialog.set("content",_25);mm_popup_dialog.set("title",t.title);},function(err){content="<p>error: <p>"+err.response.text+"</p></p>";mm_popup_dialog.set("content",content);mm_popup_dialog.set("title","error");});console.log(mm_popup_dialog.domNode);mm_popup_dialog.show();});_b("#addline").on("click",function(evt){evt.preventDefault();var row=new dijit.form.ValidationTextBox({id:"emailbox",selectOnClick:true,name:"emailbox",trim:true,required:true,invalidMessage:"Dit is geen correct emailadres"});row.placeAt("invite_list");row.startup();});_b("#flash").on("click",function(evt){evt.preventDefault();var t=evt.target;dojo.destroy(t);});var _26=_b(".ajaxclick");on(_26,"click",function(evt){evt.preventDefault();var t=evt.target;console.log(t.href);var id=dojo.getAttr(t,"data-ezine-id");console.log(id);var btn=new dijit.form.Button({label:"Ok",type:"submit",name:"submit",});var box=new dijit.form.TextBox({name:"id",type:"hidden",value:id,});var f=new dijit.form.Form({id:"confirm_form",method:"POST",action:t.href,onSubmit:function(evt){dojo.stopEvent(evt);var _27={form:"confirm_form",handleAs:"json",load:function(_28){var _29="";_29+="<h2>Succes</h2>";_29+="<p>"+_28.action+"</p>";_29+="<p>"+_28.response+"</p>";_29+="<p>You can close this window.</p>";console.log(_28);dojo.byId("progresstext").innerHTML=_29;},error:function(_2a){dojo.byId("progresstext").innerHTML=_2a;console.log(_2a);}};dojo.byId("progresstext").innerHTML="Busy... please wait.";var _2b=dojo.xhrPost(_27);},});var _2c=new dijit.Dialog({title:"Upload ezine to Clang",content:"<p>Upload ezine to Clang?</p>\n<p id='progresstext'></p>",});dojo.place(box.domNode,f.containerNode);dojo.place(btn.domNode,f.containerNode);dojo.place(f.domNode,_2c.containerNode);_2c.show();});mm_clicked=function(_2d){console.log(_2d);window.history.pushState("","",_2d);mm_popup_dialog.set("href",_2d);mm_popup_dialog.set("title","Dialog");mm_popup_dialog.show();};ezines=new dojo.store.JsonRest({target:"json/Ezine"});};_a(_20);});require(["dojo/ready","dojo/request/xhr","dojo/dom","dojo/dom-construct","dojo/json","dojo/on","dojo/data/ItemFileReadStore","dojox/grid/EnhancedGrid","dojo/domReady!"],function(_1,_2,_3,_4,_5,on,_6,_7){create_show_grid=function(){var _8=[[{"name":"id","field":"id","width":"35px"},{"name":"ogm_code","field":"ogm_code","width":"150px"},{"name":"partner_titel","field":"partner_titel","width":"100px"},{"name":"veiling_titel","field":"veiling_titel","width":"200px"},{"name":"veiling_id","field":"veiling_id","width":"65px"},{"name":"datum_hoogste_bod","field":"datum_hoogste_bod","width":"100px"},{"name":"betaal_datum","field":"betaal_datum","width":"100px"},{"name":"annulatie_datum","field":"annulatie_datum","width":"100px"},]];var _9=new _7({id:"popshowgrid",structure:_8,rowSelector:"15px",loadingMessage:"Loading grid...",autoWidth:true,});return _9;};function _a(){var _b=dijit.byId("search_grid");var _c=dijit.byId("show_grid");on(_b,"rowclick",function(e){var _d=_b.getItem(e.rowIndex);var _e=store.getValue(_d,"clang_id");_2("/json_auctions/search/auction",{query:{"clang_id":_e},handleAs:"json"}).then(function(_f){auctionstore=new _6({data:_f});_c.setStore(auctionstore);},function(err){content="<p>error: <p>"+err.response.text+"</p></p>";mm_popup_dialog.set("content",content);mm_popup_dialog.set("title",id);mm_popup_dialog.show();});});on(_c,"rowdblclick",function(e){var _10=_c.getItem(e.rowIndex);if(show_grid.name=="customer_show_grid"){var _11="/AuctionManager/auction/"+_10.veiling_id+"/view";}else{if(show_grid.name=="auction_show_grid"){var _11="/CustomerManager/customer/"+_10.clang_id+"/view";}}mm_clicked(_11);});function _12(e){var _13=grid.getItem(e.rowIndex);console.log(_13);};};_1(_a);});