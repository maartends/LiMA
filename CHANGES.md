0.0
---

- Initial version

0.0.1
-----

- Added pymongo
- Localization changed to 'nl' to solve datepicker i18n issue
- Upload to Clang implemented for vakbe e-zines

0.0.2
-----

- Added Dojo Toolkit

0.0.3
-----

- switched db backend from SQlite to PostgrSQL
- Added Dojo Toolkit (completely removed JQuery)
- Added "Download as html" function for ezines
- Added Tools-menu (for updating auction database)

0.0.4
-----

- upgraded to Dojo 1.8
- added preloader
- added tabcontainer: ezines & veilingen

0.0.5
-----

- added search function for auctions through DataGrid and Store

0.0.6
-----

- search function is now case insensitive (default)
- customer search function uses view "veilingen_customers" as a temporary
  precursor to an actual customer table

0.0.7
-----

- view popups on grids
- added links on dashboard

0.0.8
-----
- week and month numbers added to dashboard
- top auctions added to dashboard
- SourceForge project created

0.0.9
-----
- added PostgreSQL check upon login
- fixed chart reloads (due to undefined 'on' on dijit_byId)
- charts x-axis updated to reflect actual week- and month numbers
- top auctions: now showing all
- fixed undefined 'on' on dijit_byId: "script type dojo/on" on every grid
- filterselect (partner_title) now dynamic: data/store
- fixed all grid-to-grid and grid-to-popup views: auctions, customers, defaulters

0.0.10
------
- added url-selectable tabs (eg: http://devel.lima.malimedia.be/Dashboard/#tab_topauctions)
- added totals to topacutions grid (prel)
- year, month and week grids adapted

0.0.11 (2013-10-10)
------
- layout changes: colors, app-header markup
- changed default ordering of ezines list (send_date desc)
- added manual form to create/add Biedmee-ezines + Contents
- added accordeon tab for contents
- changed to new API token
- removed pyramid_formalchemy autogenerated interface

0.0.12 (2013-10-17)
------
- Added 'viewsource' plugin to editor
- Model change: added many-to-many between Ezine and EzineItems + sort order (position) column
- Added (preliminary) OrderManager
- Changed function of AuctionManager
- Added drag-n-drop functionality from auctions to ezines
- Added update ezine and auctions

0.0.13 (2014-06-16)
------
- Added model/table to report Clang->Mailjet syncs
- Changed EzineManager: added overview table with reports
- Changed 'scripts/populate.py': removed references to Mongo and XML

0.0.14 (2015-06-05)
------

- Premailer functionality: LiMA now uses the local version of the premailer and
  is making a subprocess call to the ruby premailer gem (to solve the @media
  query css)
- Added attributes on ezine model (html, html_pre and txt)
- Changed run.py as it was premailing as well (leftover from old script)