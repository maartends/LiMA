#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  helpers.py
#
#  Copyleft 2012 Mali Media Group <admin@malimedia.be>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You can find the GNU General Public License on:
#  http://www.gnu.org/copyleft/gpl.html
#
#

class RawSqlConstruct:
    """
    SqlConstruct
    """
    def __init__(self, request=None):
        """
        First we lookup appropriate function
        """
        if request:
            self.request = request
            self.func = getattr(self, request.matchdict['view'] + '_sql')
        else:
            pass

    def as_string(self):
        return self.func(self.request)

    def search_sql(self, request):
        """
        search_sql
        """
        if request.GET:
            # for now we only support one filter criterium
            params = request.GET
            for k, v in params.items():
                if v == '':
                    del(params[k])
            l = list()
            numcols = ('id', 'veiling_id', 'clang_id', 'hoogste_bod', 'administratiekost', 'garante_prijs')
            for k, v in params.items():
                if k in numcols:
                    l.append("{c} = '{v}'".format(c=k, v=v))
                else:
                    l.append("{c} ILIKE '{v}%%'".format(c=k, v=v))
        params = ' AND '.join(l)
        filter = request.matchdict['filter']
        if filter == 'customer':
            table = 'veilingen_customers'
        elif filter == 'auction':
            table = 'veilingen'
        sql = "select * from {t} where {p};".format(t=table, p=params)
        return sql

    def defaulters_sql(self, request):
        """
        defaulters_sql
        """
        filter = request.matchdict['filter']
        if filter != 'all':
            sql = "SELECT * FROM veilingen WHERE betaal_datum IS NULL AND annulatie_datum IS NULL AND datum_hoogste_bod::date = (DATE 'today' - {n}) ORDER BY datum_hoogste_bod ASC;".format(n=filter)
        else:
            sql = "SELECT * FROM veilingen WHERE betaal_datum IS NULL AND annulatie_datum IS NULL ORDER BY datum_hoogste_bod ASC;"
        return sql

    def viewcustomer(self, request):
        """
        viewcustomer
        """
        id = request.matchdict['id']
        action = request.matchdict['action']
        if action   == 'view':
            params  = 'clang_id = {id}'.format(id=id)
            table   = 'veilingen_customers'
            sql     = "select * from {t} where {p};".format(t=table, p=params)
        elif action == 'edit':
            sql     = "SELECT * FROM veilingen WHERE betaal_datum IS NULL AND annulatie_datum IS NULL ORDER BY datum_hoogste_bod ASC;"
        return sql

    def viewauction(self, request):
        """
        viewauction
        """
        id = request.matchdict['id']
        action = request.matchdict['action']
        if action   == 'view':
            params  = 'veiling_id = {id}'.format(id=id)
            table   = 'veilingen'
            sql     = "select * from {t} where {p};".format(t=table, p=params)
        elif action == 'edit':
            sql     = "SELECT * FROM veilingen WHERE betaal_datum IS NULL AND annulatie_datum IS NULL ORDER BY datum_hoogste_bod ASC;"
        return sql

    def update_veilingen_db(self):
        """
        update_veilingen_db
        """
        sql = r"""
            BEGIN;
            DROP TABLE IF EXISTS veilingen_tmp;
            CREATE TABLE veilingen_tmp
            (
                ID                  serial PRIMARY KEY,
                OGM_code            varchar(12) UNIQUE NOT NULL,    -- OGM_code (bankreferentie)
                Partner_Titel       varchar(255),                   -- Naam van de partner
                Veiling_Titel       varchar(255),                   -- Titel van deze veiling
                Veiling_ID          integer UNIQUE NOT NULL,        -- Veiling ID
                Veiling_link        varchar(2048),                  -- URL naar deze veiling
                Hoogste_bod         varchar(255),                   -- Hoogste bod dat deze veiling haalde
                Administratiekost   varchar(255),                   -- Administratiekost voor deze veiling
                Garante_prijs       varchar(255),                   -- Garante_prijs voor deze veiling
                Datum_Hoogste_bod   timestamp,                      -- Datum & tijd waarop deze veiling het hoogste bod kreeg
                Betaal_datum        timestamp,
                Annuleringsverzekering  varchar(255),               -- Annuleringsverzekering
                Full_option         varchar(255),                   -- Full option
                Annulatie_datum     timestamp,
                Inningsdatum        timestamp,
                Extra_informatie    text,
                Clang_ID            integer,
                Klant_Voornaam      varchar(255),
                Klant_Achternaam    varchar(255),
                Klant_Email         varchar(255),
                Klant_Straat        varchar(255),
                Klant_Nummer        varchar(255),
                Klant_Postcode      varchar(255),
                Klant_Gemeente      varchar(255),
                Klant_Telefoon      varchar(255),
                Clang_Error         text
            );
            COPY veilingen_tmp(ogm_code, partner_titel, veiling_titel, veiling_id, veiling_link, hoogste_bod, administratiekost, garante_prijs, datum_hoogste_bod, betaal_datum, annuleringsverzekering, full_option, annulatie_datum, inningsdatum, extra_informatie, clang_id, klant_voornaam, klant_achternaam, klant_email, klant_straat, klant_nummer, klant_postcode, klant_gemeente, klant_telefoon, clang_error) FROM '/tmp/sheet2copy.csv' WITH DELIMITER ';' CSV HEADER;
            DROP TABLE IF EXISTS veilingen CASCADE;
            CREATE TABLE veilingen
            (
                ID                  serial PRIMARY KEY,
                OGM_code            varchar(12) UNIQUE NOT NULL,    -- OGM_code (bankreferentie)
                Partner_Titel       varchar(255),                   -- Naam van de partner
                Veiling_Titel       varchar(255),                   -- Titel van deze veiling
                Veiling_ID          integer UNIQUE NOT NULL,        -- Veiling ID
                Veiling_link        varchar(2048),                  -- URL naar deze veiling
                Hoogste_bod         numeric(7, 2),                  -- Hoogste bod dat deze veiling haalde
                Administratiekost   numeric(7, 2),                  -- Administratiekost voor deze veiling
                Garante_prijs       numeric(7, 2),                  -- Garante_prijs voor deze veiling
                Datum_Hoogste_bod   timestamp,                      -- Datum & tijd waarop deze veiling het hoogste bod kreeg
                Betaal_datum        timestamp,
                Annuleringsverzekering  numeric(7, 2),              -- Annuleringsverzekering
                Full_option         numeric(7, 2),                  -- Full option
                Annulatie_datum     timestamp,
                Inningsdatum        timestamp,
                Extra_informatie    text,
                Clang_ID            integer,
                Klant_Voornaam      varchar(255),
                Klant_Achternaam    varchar(255),
                Klant_Email         varchar(255),
                Klant_Straat        varchar(255),
                Klant_Nummer        varchar(255),
                Klant_Postcode      varchar(255),
                Klant_Gemeente      varchar(255),
                Klant_Telefoon      varchar(255),
                Clang_Error         text
            );
            INSERT INTO veilingen
            SELECT
                id,
                ogm_code,
                partner_titel,
                veiling_titel,
                veiling_id,
                veiling_link,
                to_number(replace(hoogste_bod, ',', '.'), '99999.99'),
                to_number(replace(administratiekost, ',', '.'), '99999.99'),
                to_number(replace(garante_prijs, ',', '.'), '99999.99'),
                datum_hoogste_bod,
                betaal_datum,
                to_number(annuleringsverzekering, '99999.99'),
                to_number(full_option, '99999.99'),
                annulatie_datum,
                inningsdatum,
                extra_informatie,
                clang_id,
                klant_voornaam,
                klant_achternaam,
                klant_email,
                klant_straat,
                klant_nummer,
                klant_postcode,
                klant_gemeente,
                klant_telefoon,
                clang_error
            FROM veilingen_tmp;
            CREATE OR REPLACE VIEW veilingen_customers AS
                SELECT DISTINCT ON (veilingen.clang_id) veilingen.id, veilingen.clang_id, veilingen.klant_voornaam, veilingen.klant_achternaam, veilingen.klant_email, veilingen.klant_straat, veilingen.klant_nummer, veilingen.klant_postcode, veilingen.klant_gemeente, veilingen.klant_telefoon
                FROM veilingen;
            GRANT SELECT ON veilingen, veilingen_customers TO mmreadgroup;
            COMMIT;
            """
        return sql

    def charts_sql(self, request):
        """
        auction_charts
        """
        period = request.matchdict['filter']
        # want months? give names as well
        if period == 'year':
            sql_base_string = r"""
                select min(id) as ident, extract(year from datum_hoogste_bod)::int as year, count(id)::int as n, sum(hoogste_bod + administratiekost) as omzet
                from veilingen
                group by year
                order by year ASC;"""
        elif period == 'month':
            sql_base_string = r"""
                select min(id) as ident, extract(year from datum_hoogste_bod)::int as year, extract(month from datum_hoogste_bod)::int as month, to_char(datum_hoogste_bod, 'Month') as month_name, count(id)::int as n, sum(hoogste_bod + administratiekost) as omzet
                from veilingen
                group by year, month, month_name
                order by year, month ASC;"""
        else: #weeks
            sql_base_string = r"""
                select min(id) as ident, extract(year from datum_hoogste_bod)::int as year, extract(month from datum_hoogste_bod)::int as month, extract(week from datum_hoogste_bod)::int as week, count(id)::int as n, sum(hoogste_bod + administratiekost) as omzet
                from veilingen
                group by year, month, week
                order by year, month, week ASC;"""
        sql = sql_base_string.format(p=period)
        return sql

    def topauctions_sql(self, request):
        """
        topauctions
        """
        lim = request.matchdict['filter']
        params = request.GET
        for k, v in params.items():
            if v == '':
                del(params[k])
        l = list()
        for k, v in params.items():
            if k == 'start_date':
                l.append("date(datum_hoogste_bod) >= '{v}'".format(c=k, v=v))
            elif k == 'end_date':
                l.append("date(datum_hoogste_bod) <= '{v}'".format(c=k, v=v))
        params = ' AND '.join(l)
        sql_base_string = r"""
        select trim(veiling_titel || ' / ' || partner_titel) as dist, count(id)::int as occ, min(garante_prijs) as garante_prijs,
        max(hoogste_bod) as max_hoogste_bod,
        min(hoogste_bod) as min_hoogste_bod,
        round( sum(hoogste_bod)/count(id), 2 ) as avg_bod,
        round( (sum(hoogste_bod + administratiekost - garante_prijs + 5)) / count(id), 2) as eur_avg_marge,
        sum(hoogste_bod + administratiekost - garante_prijs + 5) as eur_tot_marge,
        round( sum(hoogste_bod + administratiekost - garante_prijs + 5) / sum(garante_prijs) * 100, 1 ) as proc_marge
        from veilingen """
        if params:
            sql_base_string += ' '.join(('WHERE', params))
        sql_base_string += r"""group by dist
                               order by occ desc"""
        if lim != '0':
            sql_base_string += ' LIMIT {p}'
        sql = sql_base_string.format(p=lim)
        return sql

    def filterselect_sql(self, request):
        """
        filterselect
        """
        sql_base_string = r"""
            select distinct on ({p}) {p} as id, {p} from veilingen
            order by {p};"""
        sql = sql_base_string.format(p=request.matchdict['filter'])
        return sql
