PRAGMA foreign_keys = ON;

drop table IF EXISTS consumers;
drop table IF EXISTS professionals;
drop table IF EXISTS profile_search;
drop table IF EXISTS professionals_bookmarks;
drop table IF EXISTS badges;
drop table IF EXISTS appointments;

create TABLE consumers (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

create TABLE professionals (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  fullname TEXT NOT NULL,
  qualifications TEXT NOT NULL,
--  psychologist, psychiatrist, social worker, therapist
  profession TEXT NOT NULL,
--  for example: Depression, Anxiety, Bipolar, PTSD, OCD, Personality Disorders, Eating Disorders & Body Image Issues etc.
  specialties TEXT NOT NULL,
  languages TEXT NOT NULL,
  contact_method TEXT NOT NULL,
  contact_details TEXT NOT NULL,
  details TEXT NOT NULL

);

-- bookmarks
create TABLE professionals_bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consumer_id INTEGER NOT NULL,
    professional_id INTEGER NOT NULL,
    FOREIGN KEY (consumer_id)
        REFERENCES consumers (id) ON DELETE CASCADE,
    FOREIGN KEY (professional_id)
        REFERENCES professionals (id) ON DELETE CASCADE
);

-- appointments
-- all date-time in UTC
create TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    professional_id INTEGER NOT NULL,
    consumer_id INTEGER NOT NULL,
    requested DATETIME DEFAULT CURRENT_TIMESTAMP,
    professional_declined DATETIME DEFAULT NULL,
    professional_scheduled DATETIME DEFAULT NULL,
    appointment_date DATETIME DEFAULT NULL,
    appointment_duration INTEGER DEFAULT NULL,
    consumer_accepted DATETIME DEFAULT NULL,
    consumer_resigned DATETIME DEFAULT NULL,
    status INTEGER DEFAULT NULL,
    FOREIGN KEY (consumer_id)
        REFERENCES consumers (id) ON DELETE CASCADE,
    FOREIGN KEY (professional_id)
        REFERENCES professionals (id) ON DELETE CASCADE
);

create TABLE badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    badge_name TEXT NOT NULL,
    badge_description TEXT NOT NULL,
    professional_id INTEGER NOT NULL,
    FOREIGN KEY (professional_id)
        REFERENCES professionals (id) ON DELETE CASCADE
);

-- full test search extension FTS5
create VIRTUAL TABLE profile_search using fts5(professional_id, fullname, qualifications, profession, specialties, languages, profile);
