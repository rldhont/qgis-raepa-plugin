--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.15
-- Dumped by pg_dump version 9.6.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- raepa_ouvrass_p audit_trigger_row
CREATE TRIGGER audit_trigger_row AFTER INSERT OR DELETE OR UPDATE ON raepa.raepa_ouvrass_p FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func('true');


-- raepa_apparass_p audit_trigger_row
CREATE TRIGGER audit_trigger_row AFTER INSERT OR DELETE OR UPDATE ON raepa.raepa_apparass_p FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func('true');


-- raepa_canalass_l audit_trigger_row
CREATE TRIGGER audit_trigger_row AFTER INSERT OR DELETE OR UPDATE ON raepa.raepa_canalass_l FOR EACH ROW EXECUTE PROCEDURE audit.if_modified_func('true');


-- raepa_ouvrass_p audit_trigger_stm
CREATE TRIGGER audit_trigger_stm AFTER TRUNCATE ON raepa.raepa_ouvrass_p FOR EACH STATEMENT EXECUTE PROCEDURE audit.if_modified_func('true');


-- raepa_apparass_p audit_trigger_stm
CREATE TRIGGER audit_trigger_stm AFTER TRUNCATE ON raepa.raepa_apparass_p FOR EACH STATEMENT EXECUTE PROCEDURE audit.if_modified_func('true');


-- raepa_canalass_l audit_trigger_stm
CREATE TRIGGER audit_trigger_stm AFTER TRUNCATE ON raepa.raepa_canalass_l FOR EACH STATEMENT EXECUTE PROCEDURE audit.if_modified_func('true');


-- raepa_ouvrass_p raepa_apres_modification_ouvrage
CREATE TRIGGER raepa_apres_modification_ouvrage AFTER INSERT OR UPDATE ON raepa.raepa_ouvrass_p FOR EACH ROW EXECUTE PROCEDURE raepa.trg_apres_modification_ouvrage();


-- raepa_canalass_l raepa_avant_ajout_ou_modification_canalisation
CREATE TRIGGER raepa_avant_ajout_ou_modification_canalisation BEFORE INSERT OR UPDATE ON raepa.raepa_canalass_l FOR EACH ROW EXECUTE PROCEDURE raepa.trg_avant_ajout_ou_modification_canalisation();


-- raepa_apparass_p raepa_avant_modification_appareil
CREATE TRIGGER raepa_avant_modification_appareil BEFORE INSERT OR UPDATE ON raepa.raepa_apparass_p FOR EACH ROW EXECUTE PROCEDURE raepa.trg_avant_modification_appareil();


-- raepa_ouvrass_p raepa_avant_modification_ouvrage
CREATE TRIGGER raepa_avant_modification_ouvrage BEFORE INSERT OR UPDATE ON raepa.raepa_ouvrass_p FOR EACH ROW EXECUTE PROCEDURE raepa.trg_avant_modification_ouvrage();


--
-- PostgreSQL database dump complete
--
