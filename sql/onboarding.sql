-- Anzahl aller Datensätze
   SELECT COUNT(*) FROM "AwsDataCatalog"."onboarding-scb"."cars";
-- Anzahl aller Datensätze gruppiert nach Jahr
   SELECT year as Jahr, COUNT(*) as Bestand FROM "AwsDataCatalog"."onboarding-scb"."cars"
   GROUP BY year
   ORDER BY year DESC;
-- Anzeige der ersten 10 Datensätze
   SELECT * FROM "AwsDataCatalog"."onboarding-scb"."cars" limit 10;

-- Anzahl der in der  Deutschland registrierten Fahrzeuge gruppiert nach Jahren (2018-2023)
   SELECT year, count(*) FROM "AwsDataCatalog"."onboarding-scb"."cars" group by year order by year asc;

-- Anzahl der in der  Deutschland registrierten Fahrzeuge gruppiert nach Jahren (2018-2023) und Bundesland
   SELECT year as Jahr, federal_state as Bundesland, count(*) as Bestand FROM "AwsDataCatalog"."onboarding-scb"."cars" group by year, federal_state order by year asc, Anzahl desc;

-- Bundesländer mit dem größten Fahrzeugbestand pro Jahr
   WITH Bestand AS
   (
     SELECT year AS Jahr, federal_state AS Bundesland, count(*) AS Anzahl
     FROM "AwsDataCatalog"."onboarding-scb"."cars"
     GROUP BY year, federal_state
     ORDER BY year asc, Anzahl desc
   )
   SELECT Bestand.Jahr, Bestand.Bundesland, Bestand.Anzahl
   FROM Bestand
   JOIN (
     SELECT Bestand.Jahr, MAX(Bestand.Anzahl) as Max_Bestand
     FROM Bestand
     GROUP by Bestand.Jahr
   ) AS t2
   ON Bestand.Jahr = t2.Jahr AND Bestand.Anzahl = t2.Max_Bestand
   ORDER by Bestand.Jahr desc;

-- Landkreise mit dem größten Fahrzeugbestand pro Jahr
   WITH Bestand AS
   (
     SELECT year AS Jahr, county AS Landkreis, count(*) AS Anzahl
     FROM "AwsDataCatalog"."onboarding-scb"."cars"
     GROUP BY year, county
     ORDER BY year asc, Anzahl desc
   )
   SELECT Bestand.Jahr, Bestand.Landkreis, Bestand.Anzahl
   FROM Bestand
   JOIN (
     SELECT Bestand.Jahr, MAX(Bestand.Anzahl) as Max_Bestand
     FROM Bestand
     GROUP by Bestand.Jahr
   ) AS t2
   ON Bestand.Jahr = t2.Jahr AND Bestand.Anzahl = t2.Max_Bestand
   ORDER by Bestand.Jahr desc;

-- Bundesländer mit den höchsten Zulassungszahlen von elektrischen Fahrzeugen pro Jahr
   SELECT year as Jahr, federal_state as Bundesland, Elektro_Fahrzeuge
   FROM (
       SELECT year, federal_state, COUNT(*) AS Elektro_Fahrzeuge
       FROM "AwsDataCatalog"."onboarding-scb"."cars"
       WHERE engine_type = 'Electric'
       GROUP BY year, federal_state
   ) AS Elektro_Fahrzeuge_Pro_Jahr
   WHERE (year, Elektro_Fahrzeuge) IN (
       SELECT year, MAX(Elektro_Fahrzeuge)
       FROM (
           SELECT year, federal_state, COUNT(*) AS Elektro_Fahrzeuge
           FROM "AwsDataCatalog"."onboarding-scb"."cars"
           WHERE engine_type = 'Electric'
           GROUP BY year, federal_state
       ) AS Elektro_Fahrzeuge_Pro_Jahr
       GROUP BY year
   )
   ORDER BY year desc;

-- Landkreise mit den höchsten Zulassungszahlen von elektrischen Fahrzeugen pro Jahr
   SELECT year as Jahr, county as Landkreis, Elektro_Fahrzeuge
   FROM (
       SELECT year, county, COUNT(*) AS Elektro_Fahrzeuge
       FROM "AwsDataCatalog"."onboarding-scb"."cars"
       WHERE engine_type = 'Electric'
       GROUP BY year, county
   ) AS Elektro_Fahrzeuge_Pro_Jahr
   WHERE (year, Elektro_Fahrzeuge) IN (
       SELECT year, MAX(Elektro_Fahrzeuge)
       FROM (
           SELECT year, county, COUNT(*) AS Elektro_Fahrzeuge
           FROM "AwsDataCatalog"."onboarding-scb"."cars"
           WHERE engine_type = 'Electric'
           GROUP BY year, county
       ) AS Elektro_Fahrzeuge_Pro_Jahr
       GROUP BY year
   )
   ORDER BY year desc;

-- Die 10 Landkreise mit der höchsten Zahl and zugelassenen Cabrios
   SELECT county, SUM(convertible) AS Anzahl_Cabrios
   FROM "AwsDataCatalog"."onboarding-scb"."cars"
   WHERE year = 2023
   GROUP BY county
   ORDER BY Anzahl_Cabrios DESC
   LIMIT 10;

-- Höchste Zulassungszahlen für elektrisch betriebene Fahrzeuge unterteilt nach Haltertyp
-- COALESCE funktioniert seltsamerweise nicht!
   SELECT year, federal_state, COALESCE(ownership, 'Unbekannt') as Haltertyp, COUNT(*) AS Anzahl
   FROM "AwsDataCatalog"."onboarding-scb"."cars"
   WHERE engine_type = 'Electric'
   GROUP BY year, federal_state, ownership
   ORDER BY year DESC, Anzahl DESC;
-- Anzahl aller Modelle in 2023 je Hersteller
   SELECT manufacturer as Hersteller, sum(quantity) as Anzahl from "AwsDataCatalog"."onboarding-scb".vehicles where year = 2023 group by manufacturer order by Anzahl DESC

-- Die verkaufsstärksten Modelle in 2023
   SELECT manufacturer as Hersteller, model as Modell, max(quantity) as Anzahl from "AwsDataCatalog"."onboarding-scb".vehicles where year = 2023 group by manufacturer, model order by Anzahl DESC

-- Die 10 bevölkerungsreichsten Städte Deutschlands
   SELECT city, population, area FROM "AwsDataCatalog"."onboarding-scb"."cities" order by population desc limit 10;
-- Bundesländer nach Bevölkerungszahl
   SELECT state as Bundesland, population as "Bevölkerungszahl" FROM "AwsDataCatalog"."onboarding-scb"."states" order by population desc;
-- Bundesländer Verhältnis Frauen/Männer
   SELECT state as Bundesland, ROUND((CAST(females AS double) / males), 3) as "Verhältnis Frauen/Männer" FROM "AwsDataCatalog"."onboarding-scb"."states" order by "Verhältnis Frauen/Männer" desc;

-- Städte Verhältnis Frauen/Männer
   SELECT city as Stadt, ROUND((CAST(females AS double) / males), 3) as "Verhältnis Frauen/Männer" FROM "AwsDataCatalog"."onboarding-scb"."cities" order by "Verhältnis Frauen/Männer" desc; 