/*
 * Author: Maarten De Schrijver
*/

/*
 * Dojo
 */
require([
        "dojo/ready", "dojo/query", "dojo/fx", "dojo/dom", "dojo/dom-geometry", "dojo/on", "dojo/domReady!"
         ],
    function(ready, query, coreFx, dom, domGeom, on){

        ready(function(){

              function slideIt(amt){
                coreFx.slideTo({
                  node: "login",
                  top: domGeom.getMarginBox("login").t.toString(),
                  left: (domGeom.getMarginBox("login").l + amt).toString(),
                  unit: "px"
                }).play();
              }

              query("#slideRightButton").on("click", function(){
                slideIt(200);
              });
              query("#slideLeftButton").on("click", function(){
                slideIt(-200);
              });

        }); // ready

    });
