-- The mapped Runaway Timeline extension ID is intentionally a reviewed
-- exception to the dotted extension namespace.
alter table public.extension_operational_events
  drop constraint if exists extension_operational_events_extension_id_check;

alter table public.extension_operational_events
  add constraint extension_operational_events_extension_id_check check (
    extension_id is null
    or extension_id ~ '^(haus[.]astrid[.][a-z0-9.-]{1,100}|haus[.]astrid-runaway-timeline)$'
  );
